//
//  ApiClient.swift
//  ApiModule
//
//  Created by Rafał Kwiatkowski on 06/05/2020.
//

import Foundation
import SwiftyJSON

public protocol ApiClientProtocol {
    func fetchBooks(completion: ([Book]) -> Void)
}

public class ApiClient: ApiClientProtocol {
    public init() {
        // nop
    }
    
    public func fetchBooks(completion: ([Book]) -> Void) {
        guard let url = Bundle(for: type(of: self)).url(forResource: "books.json", withExtension: nil),
            let data = try? Data(contentsOf: url),
            let json = try? JSON(data: data)else { return }
        
        let books: [Book] = json.array?.map {
            Book(title: $0["title"].string ?? "",
                 author: $0["author"].string ?? "",
                 numberOfPages: $0["details"]["numberOfPages"].int)
        } ?? []
        
        completion(books)
    }
}
