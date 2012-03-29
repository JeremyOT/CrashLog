//
//  CrashLog.h
//  CrashLog
//
//  Created by Jeremy Olmsted-Thompson on 3/28/12.
//  Copyright (c) 2012 JOT. MIT Licence.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

@interface NSThread (Backtrace)

-(NSArray *)callStackSymbols;

@end

@interface CrashLog : NSObject

+(CrashLog*)sharedCrashLog;

-(void)addCustomHandler:(void(^)(NSException*))block;
-(void)removeCustomHandler:(void(^)(NSException*))block;
-(void)removeAllCustomHandlers;
// Note, calling registerCrashLog will deregister any other instances.
// Use custom handlers if you want to intercept the uncaught exception.
-(void)registerCrashLog;
-(void)deregisterCrashLog;
-(void)syncToServiceURL:(NSURL*)serviceURL accountIdentifier:(NSString*)accountIdentifier;

@end
