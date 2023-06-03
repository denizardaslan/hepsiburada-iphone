# Hepsiburada iPhone Price Tracker

**Note: This project is no longer actively developed as Hepsiburada has changed the hidden product endpoint, making it inaccessible for data extraction.**

This is a data engineering project for tracking iPhone prices on Hepsiburada. As I am planning to buy a new iPhone, I need to closely monitor the prices, as Hepsiburada frequently changes them. This project aims to help me find the best price by extracting data from the Hepsiburada e-commerce platform using a hidden API and storing it in a SQLite3 database. The data is normalized and organized into three tables: `product_info`, `sales`, and `store`. By tracking the prices and analyzing the historical data, I can make informed purchasing decisions and secure a better deal.

## Project Overview

The Hepsiburada iPhone Price Tracker was designed to provide insights into the pricing trends of iPhones available on the Hepsiburada platform. By leveraging a hidden API, the project retrieved data related to iPhone products, their prices, sales information, and store details. The extracted data was stored in a SQLite3 database, allowing for efficient data organization and retrieval.

## Database Structure

The project's SQLite3 database consisted of three tables:

1. `product_info`: This table stored information about the iPhone products, including their unique identifiers, brand, model, color, and product URLs.

   | Column Name | Data Type |
   |-------------|----------|
   | `id`        | INTEGER  |
   | `product_id`| TEXT     |
   | `brand`     | TEXT     |
   | `model`     | TEXT     |
   | `colour`    | TEXT     |
   | `url`       | TEXT     |

2. `sales`: The `sales` table contained data related to the sales of iPhones, such as the product ID, customer review count, review score, and other relevant boosting factors.

   | Column Name           | Data Type |
   |-----------------------|----------|
   | `id`                  | INTEGER  |
   | `datetime`            | TIMESTAMP|
   | `product_id`          | TEXT     |
   | `merchant_id`         | TEXT     |
   | `price`               | INTEGER  |

3. `store`: This table stored information about the stores where the iPhones were sold, including the store ID (UUID) and the store name.

   | Column Name | Data Type |
   |-------------|----------|
   | `id`        | UUID     |
   | `name`      | TEXT     |

## Data Normalization

To ensure efficient data management and eliminate data redundancy, the project followed data normalization principles. The normalization process divided the data into separate tables, reducing data duplication and enabling easier data retrieval and updates. The `product_info`, `sales`, and `store` tables were interconnected through primary key and foreign key relationships, allowing for seamless data retrieval and manipulation.

## Price Tracking and Dashboard

The Hepsiburada iPhone Price Tracker periodically retrieved data at one-hour intervals, providing up-to-date pricing information for iPhones on the Hepsiburada platform. The extracted data was stored in the SQLite3 database, enabling historical price tracking and analysis.

~~The project included a dashboard that visualized the pricing trends over time, allowing users to track price fluctuations, identify the best deals, and make informed purchasing decisions.~~