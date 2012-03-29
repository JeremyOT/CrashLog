//
//  CLViewController.m
//  CrashLogDemo
//
//  Created by Jeremy Olmsted-Thompson on 3/28/12.
//  Copyright (c) 2012 JOT. All rights reserved.
//

#import "CLViewController.h"

@implementation CLViewController

-(void)crashArray:(id)sender {
    [[[NSArray alloc] init] objectAtIndex:42];
}

-(void)crashBadAccess:(id)sender {
    NSString *text = [[NSString alloc] init];
    [text release];
    [text substringFromIndex:42];
}

-(void)crashQueued:(id)sender {
    dispatch_async(dispatch_queue_create("My Queue", 0), ^{
        [self crashArray:nil];
    });
}

-(void)crashAsync:(id)sender {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_BACKGROUND, 0), ^{
        [self crashArray:nil];
    });
}

@end
