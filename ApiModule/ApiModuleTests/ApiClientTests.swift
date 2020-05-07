//
//  ApiClientTests.swift
//  ApiClientTests
//
//  Created by Rafał Kwiatkowski on 05/05/2020.
//  Copyright © 2020 FANDOM. All rights reserved.
//

import XCTest
@testable import ApiModule

class ApiClientTests: XCTestCase {
    
    private var sut: ApiClient!

    override func setUpWithError() throws {
        try super.setUpWithError()
        sut = ApiClient()
    }

    override func tearDownWithError() throws {
        sut = nil
        try super.tearDownWithError()
    }

    func testShouldFetchBooks() throws {
        // Given
        var resultBooks: [Book] = []
        
        // When
        sut.fetchBooks { books in
            resultBooks = books
        }
        
        // Then
        XCTAssertEqual(resultBooks.count, 3)
    }
}
