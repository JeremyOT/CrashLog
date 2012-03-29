//
//  CLAppDelegate.h
//  CrashLogDemo
//
//  Created by Jeremy Olmsted-Thompson on 3/28/12.
//  Copyright (c) 2012 JOT. All rights reserved.
//

#import <UIKit/UIKit.h>

@class CLViewController;

@interface CLAppDelegate : UIResponder <UIApplicationDelegate>

@property (strong, nonatomic) UIWindow *window;

@property (strong, nonatomic) CLViewController *viewController;

@end
