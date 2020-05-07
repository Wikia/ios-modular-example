//
//  ViewControllerTests.swift
//  FeatureModuleTests
//
//  Created by Rafał Kwiatkowski on 07/05/2020.
//

import XCTest
import ApiModule
@testable import FeatureModule

class ViewControllerTests: XCTestCase {
    
    private var sut: ViewController!
    private var apiClient: ApiClientMock!

    override func setUpWithError() throws {
        try super.setUpWithError()
        apiClient = ApiClientMock()
        sut = ViewController()
        sut.apiClient = apiClient
    }

    override func tearDownWithError() throws {
        apiClient = nil
        sut = nil
        try super.tearDownWithError()
    }

    func testShouldFetchBooks() {
        // When
        sut.fetchBooks()
        
        // Then
        XCTAssertEqual(apiClient.fetchBooksCallsCount, 1)
    }
}

private class ApiClientMock: ApiClientProtocol {
    
    var fetchBooksCallsCount = 0
    
    func fetchBooks(completion: ([Book]) -> Void) {
        fetchBooksCallsCount += 1
    }
}
