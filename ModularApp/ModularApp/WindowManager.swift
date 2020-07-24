//
//  WindowManager.swift
//  ModularApp
//
//  Created by Rafał Kwiatkowski on 24/07/2020.
//

import UIKit
import FeatureModule

class WindowManager {
    func createWindow() -> UIWindow {
        let window = UIWindow(frame: UIScreen.main.bounds)
        window.rootViewController = ViewController(nibName: nil, bundle: nil)
        return window
    }
}
