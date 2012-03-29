//
//  CrashLog.m
//  CrashLog
//
//  Created by Jeremy Olmsted-Thompson on 3/28/12.
//  Copyright (c) 2012 JOT. MIT Licence.
//

#import "CrashLog.h"
#import "TotoService.h"
#include <execinfo.h>

#define CrashLogCallStackSymbols @"CallStackSymbols"
#define CrashLogSignalException @"CrashLogSignalException"
#define CrashLogSignal @"Signal"
#define CrashLogThread @"Thread"
#define CrashLogCurrentQueue @"CurrentQueue"
#define CrashLogExceptionDescription @"ExceptionDescription"
#define CrashLogVersion @"Version"
#define CrashLogShortVersion @"ShortVersion"
#define CrashLogPlatform @"Platform"
#define CrashLogPlatformVersion @"PlatformVersion"
#define CrashLogModel @"Model"
#define CrashLogAdditionalInformation @"AdditionalInformation"
#define CrashLogCrashDate @"CrashDate"
#define CrashLogFileName @"CrashLog.plist"

@implementation NSThread (Backtrace)

-(NSArray *)callStackSymbols {
    void* callstack[128];
    int frames = backtrace(callstack, 128);
    char **backtraceStrings = backtrace_symbols(callstack, frames);
    
    NSMutableArray *backtrace = [NSMutableArray arrayWithCapacity:frames];
    for (int i = 0; i < frames; i++){
        [backtrace addObject:[NSString stringWithUTF8String:backtraceStrings[i]]];
    }
    free(backtraceStrings);
    
    return backtrace;
}

@end

@interface CrashLog ()

+(NSString*)logFilePath;
-(NSMutableArray*)customHandlers;

@end

@implementation CrashLog

+(CrashLog *)sharedCrashLog {
    static CrashLog *sharedCrashLog = nil;
    if (!sharedCrashLog) {
        sharedCrashLog = [[CrashLog alloc] init];
    }
    return sharedCrashLog;
}

-(void)syncToServiceURL:(NSURL *)serviceURL accountIdentifier:(NSString *)accountIdentifier {
    NSMutableArray *crashExceptions = [NSMutableArray arrayWithContentsOfFile:[CrashLog logFilePath]];
    if (![crashExceptions count]) {
        return;
    }
    TotoService *service = [TotoService serviceWithURL:serviceURL];
    service.usesBSON = YES;
    [service totoRequestWithMethodName:@"log.post" parameters:[NSDictionary dictionaryWithObjectsAndKeys:
                                                               accountIdentifier, @"account_id",
                                                               crashExceptions, @"logs",
                                                               nil]
                        receiveHandler:^(id obj) {
                            NSLog(@"CrashLog Synced %d logs", [crashExceptions count]);
                            [[NSFileManager defaultManager] removeItemAtPath:[CrashLog logFilePath] error:nil];
                        } errorHandler:^(NSError *error) {
                            NSLog(@"CrashLog Error syncing log %@", error);
                        }];
}

void handleException(NSException *exception);
void handleSignal(int signal);
void handleException(NSException *exception) {
	NSMutableDictionary *exceptionData = [NSMutableDictionary dictionaryWithDictionary:[exception userInfo]];
    if (![exceptionData objectForKey:CrashLogCallStackSymbols]) {
        [exceptionData setObject:[exception callStackSymbols] forKey:CrashLogCallStackSymbols];
    }
    if ([[[NSThread currentThread] name] length]) {
        [exceptionData setObject:[[NSThread currentThread] name] forKey:CrashLogThread];
    }
    [exceptionData setObject:[NSString stringWithFormat:@"%s", dispatch_queue_get_label(dispatch_get_current_queue())] forKey:CrashLogCurrentQueue];
    [exceptionData setObject:[NSString stringWithFormat:@"%s", dispatch_queue_get_label(dispatch_get_current_queue())] forKey:CrashLogCurrentQueue];
    [exceptionData setObject:[exception description] forKey:CrashLogExceptionDescription];
    [exceptionData setObject:[[[NSBundle mainBundle] infoDictionary] objectForKey:@"CFBundleVersion"] forKey:CrashLogVersion];
    [exceptionData setObject:[[[NSBundle mainBundle] infoDictionary] objectForKey:@"CFBundleShortVersionString"] forKey:CrashLogShortVersion];
    [exceptionData setObject:[[UIDevice currentDevice] systemName] forKey:CrashLogPlatform];
    [exceptionData setObject:[[UIDevice currentDevice] systemVersion] forKey:CrashLogPlatformVersion];
    [exceptionData setObject:[[UIDevice currentDevice] model] forKey:CrashLogModel];
    [exceptionData setObject:[NSDate date] forKey:CrashLogCrashDate];
    
    NSLog(@"Exception:%@"
          "\nID: %@",
          exceptionData,
          [[NSBundle mainBundle] bundleIdentifier]);
    NSMutableArray *crashExceptions = [NSMutableArray arrayWithContentsOfFile:[CrashLog logFilePath]];
    if (!crashExceptions) {
        crashExceptions = [NSMutableArray array];
    }
    [crashExceptions addObject:exceptionData];
    [crashExceptions writeToFile:[CrashLog logFilePath] atomically:YES];
    // Call any registered custom handlers
	for (id handler in [[CrashLog sharedCrashLog] customHandlers]) {
        NSDictionary *data = ((NSDictionary *(^)(NSException*))handler)(exception);
        if (data) {
            if(![exceptionData objectForKey:CrashLogAdditionalInformation]) {
                [exceptionData setObject:[NSMutableArray array] forKey:CrashLogAdditionalInformation];
            }
            [[exceptionData objectForKey:CrashLogAdditionalInformation] addObject:data];
        }
    }
    [crashExceptions writeToFile:[CrashLog logFilePath] atomically:YES];
    [[CrashLog sharedCrashLog] deregisterCrashLog];
	if ([[exception name] isEqual:CrashLogSignalException]) {
		kill(getpid(), [[[exception userInfo] objectForKey:CrashLogCallStackSymbols] intValue]);
	} else {
		[exception raise];
	}
}
void handleSignal(int signal) {
	handleException([NSException exceptionWithName:CrashLogSignalException
                                            reason:[NSString stringWithFormat: NSLocalizedString(@"Signal %d was raised.", nil), signal]
                                          userInfo:[NSDictionary dictionaryWithObjectsAndKeys:
                                                    CrashLogSignal, [NSNumber numberWithInt:signal],
                                                    CrashLogCallStackSymbols, [NSThread callStackSymbols],
                                                    nil]]);
}

-(NSMutableArray *)customHandlers {
    NSMutableArray *handlers = nil;
    if (!handlers) {
        handlers = [[NSMutableArray alloc] init];
    }
    return handlers;
}

-(void)addCustomHandler:(void(^)(NSException*))block {
    [[self customHandlers] addObject:[[block copy] autorelease]];
}

-(void)removeCustomHandler:(void(^)(NSException*))block {
    [[self customHandlers] removeObject:block];
}

-(void)removeAllCustomHandlers {
    [[self customHandlers] removeAllObjects];
}

-(void)registerCrashLog {
    NSSetUncaughtExceptionHandler(&handleException);
	signal(SIGABRT, handleSignal);
	signal(SIGILL, handleSignal);
	signal(SIGSEGV, handleSignal);
	signal(SIGFPE, handleSignal);
	signal(SIGBUS, handleSignal);
	signal(SIGPIPE, handleSignal);
}

-(void)deregisterCrashLog {
	NSSetUncaughtExceptionHandler(NULL);
	signal(SIGABRT, SIG_DFL);
	signal(SIGILL, SIG_DFL);
	signal(SIGSEGV, SIG_DFL);
	signal(SIGFPE, SIG_DFL);
	signal(SIGBUS, SIG_DFL);
	signal(SIGPIPE, SIG_DFL);
}

+(NSString *)logFilePath {
    NSString *logFilePath = nil;
    if (!logFilePath) {
        logFilePath = [[NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) lastObject] stringByAppendingPathComponent:CrashLogFileName];
//        [[NSFileManager defaultManager] createDirectoryAtPath:logFilePath withIntermediateDirectories:YES attributes:nil error:nil];
    }
    return logFilePath;
}

@end
