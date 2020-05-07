//
//  ViewController.swift
//  FeatureModule
//
//  Created by Rafał Kwiatkowski on 06/05/2020.
//

import UIKit
import ApiModule

public class ViewController: UIViewController {

    var apiClient: ApiClientProtocol = ApiClient()
    private var books: [Book] = []
    private lazy var tableView: UITableView = {
        let tableView = UITableView()
        tableView.register(UITableViewCell.self, forCellReuseIdentifier: ViewController.reuseIdentifier)
        tableView.dataSource = self
        return tableView
    }()
    
    private static let reuseIdentifier = "Book"
    
    public override func viewDidLoad() {
        super.viewDidLoad()
        setUpTableView()
        fetchBooks()
    }
    
    func fetchBooks() {
        apiClient.fetchBooks { [weak self] books in
            guard let self = self else { return }
            self.books = books
            self.tableView.reloadData()
        }
    }
    
    private func setUpTableView() {
        view.addSubview(tableView)
        tableView.translatesAutoresizingMaskIntoConstraints = false
        tableView.leadingAnchor.constraint(equalTo: view.leadingAnchor).isActive = true
        tableView.trailingAnchor.constraint(equalTo: view.trailingAnchor).isActive = true
        tableView.topAnchor.constraint(equalTo: view.topAnchor).isActive = true
        tableView.bottomAnchor.constraint(equalTo: view.bottomAnchor).isActive = true
    }
}

extension ViewController: UITableViewDataSource {
    public func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: ViewController.reuseIdentifier, for: indexPath)
        cell.textLabel?.text = books[indexPath.row].title
        cell.detailTextLabel?.text = books[indexPath.row].author
        return cell
    }
    
    public func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        books.count
    }
}
