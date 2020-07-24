//
//  ModularAppTests.swift
//  ModularAppTests
//
//  Created by Rafał Kwiatkowski on 05/05/2020.
//  Copyright © 2020 FANDOM. All rights reserved.
//

import XCTest
@testable import ModularApp
import FeatureModule

class ModularAppTests: XCTestCase {

    func testShouldCreateWindowWithViewController() throws {
        // When
        let window = WindowManager().createWindow()
        
        XCTAssertTrue(window.rootViewController!.isKind(of: ViewController.self))
    }
}
