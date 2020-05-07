//
//  AppDelegate.swift
//  ModularApp
//
//  Created by Rafał Kwiatkowski on 05/05/2020.
//  Copyright © 2020 FANDOM. All rights reserved.
//

import UIKit
import FeatureModule

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        let window = UIWindow(frame: UIScreen.main.bounds)
        window.rootViewController = ViewController(nibName: nil, bundle: nil)
        window.makeKeyAndVisible()
        self.window = window
        return true
    }

}

