//
//  CLViewController.h
//  CrashLogDemo
//
//  Created by Jeremy Olmsted-Thompson on 3/28/12.
//  Copyright (c) 2012 JOT. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface CLViewController : UIViewController

-(IBAction)crashArray:(id)sender;
-(IBAction)crashBadAccess:(id)sender;
-(IBAction)crashQueued:(id)sender;
-(IBAction)crashAsync:(id)sender;

@end
