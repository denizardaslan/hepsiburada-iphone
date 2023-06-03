import requests
import datetime
import json
import sqlite3


def data_download(date_time):
    url = "https://blackgate.hepsiburada.com/moriaapi/api/product-and-facet?addressName=&filter=categoryId:2147483642_371965_60005202&pageType=Category&receiverCity=&receiverDistrict=&receiverTown=&size=24"
    headers = {
        "authority": "blackgate.hepsiburada.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "tr,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "cookie": "wt3_sid=%3B289941511384204; hbus_anonymousId=887d894f-66aa-4986-ac15-465c48d70681; wt_fa=lv~1682512014912|1713616014912#cv~1|1713616014912#fv~2023-04|1713616014912#; wt_fa_s=start~1|1714048038638#; hbus_sessionId=aa58e0e2-3ccf-419a-b567-8d32bf5797a4%7C1682513840066; bm_sz=DD0454B5390866406635C3C08A9C0D83~YAAQI04SAtocS7uHAQAAsQTDwxPtXi6m2m7B+2U9jotW0akv2cLpDCSyWTQnCXzVQ3db41+z/HDStZkUdbZ8tf+Y3Hu8B0B3t0yrwXjzkd49tMNeYqGCgN+PYQE2juXM012jBbMWnEmp/yXDtb4dW/RtSRKpt4jYHYTrIM641tLsURbScKYZDyhGvi3/0mm4KoEt1BP7oGUjGAvSfhqT3yUV36jiqQiR9l/G1DjEeYOqXfzFz7g/E0zMWM4dOtPQMPziPVbMNcqBHILyyh+50O24984JBZowtMEZpuikUM1z1tZyU6zLpQ==~3225669~3682355; searchHistory=[%22iphone%22]; _abck=08BD063C73AAB135DD5A0D45E71C9280~0~YAAQC34ZuGawK6GHAQAADk3DwwmO/ElvwCNj5Ek6Xz+I9z8YrB+rtsbJJvrXnfOkZNDQT5cnIPSlIaSSJu4kT2cjCzJFf6CoARKIB4weI5g9OZJg6eXFNfmKOPvr4GV3pc2MP+pbEBBtCkBB1IkA2oGdH37ZEaoqMx55taADVOR3SZkN8PfSZAMK22DCmK0CkfWxl1O1f5ZmTqucuCV8QihJZ4/xlOpCwk1yl1u+6AEk82DZhNJ4geXTlJSC8mt41YnDuNOCfz+oD5Vjkfqzxc0fCoB06rR9IwKGva4AMO7kKU58Lso6IxEagqDt2rbFtlC2a7ywu/D4oZMMMy7bsx95nnndr1Vqsh5uaX2k4+dbH66LcVPwASk1WAfV9KbYmsPjeaLZgf+4pBUKQzFsAorScZgQEwYDiSxT5QKq~-1~-1~-1; wt3_eid=%3B289941511384204%7C2168233820900031405%232168261660100719587",
        "dnt": "1",
        "origin": "https://www.hepsiburada.com",
        "referer": "https://www.hepsiburada.com/iphone-ios-telefonlar-c-60005202",
        "sec-ch-ua": "'Chromium';v='112', 'Microsoft Edge';v='112', 'Not:A-Brand';v='99'",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "'macOS'",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.54",
        "x-client-id": "MoriaDesktop",
    }
    r = requests.get(url, headers=headers)
    data = r.text

    with open(str(date_time) + ".txt", "w", encoding="utf-8") as file:
        file.write(data)


def read_data():
    global json_raw_data
    raw_data = open(str(date_time) + ".txt")
    json_raw_data = json.load(raw_data)


def connect_to_database(database_name):
    conn = sqlite3.connect(database_name)
    return conn


def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS product_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            brand TEXT,
            model TEXT,
            colour TEXT,
            url TEXT
        )    
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TIMESTAMP,
            product_id TEXT,
            merchant_id TEXT,
            price FLOAT
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS store (
            id UUID PRIMARY KEY,
            name TEXT
        )
    """
    )
    conn.commit()


def insert_data_product_info(conn, product_id, brand, model, colour, url):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO product_info (product_id, brand, model, colour, url) VALUES (?, ?, ?, ?, ?)",
        (product_id, brand, model, colour, url),
    )
    conn.commit()


def insert_data_sales(conn, datetime, product_id, merchant_id, price):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sales (datetime, product_id, merchant_id, price) VALUES (?, ?, ?, ?)",
        (datetime, product_id, merchant_id, price),
    )
    conn.commit()


def insert_or_update_store_data(conn, id, name):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM store WHERE id = ?",
        (id,),
    )
    existing_id = cursor.fetchone()

    if existing_id:
        cursor.execute(
            "UPDATE store SET name = ? WHERE id = ? AND name != ?",
            (name, id, name),
        )
        if cursor.rowcount == 0:
            return
    else:
        cursor.execute(
            "INSERT INTO store (id, name) VALUES (?, ?)",
            (id, name),
        )

    conn.commit()


def retrieve_data_product_info(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product_info")
    rows = cursor.fetchall()
    return rows


def retrieve_data_sales(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales")
    rows = cursor.fetchall()
    return rows


def retrieve_data_store(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM store")
    rows = cursor.fetchall()
    return rows


def close_connection(conn):
    conn.close()


def entry_product_table():
    for item in json_raw_data["products"]:
        id = item["productId"]
        brand_name = item["brand"]
        for subitem in item["variantList"]:
            product_name = subitem["name"]
            colour = subitem["properties"]["Renk"]["displayValue"]
            url = subitem["url"]
            insert_data_product_info(conn, id, brand_name, product_name, colour, url)


def entry_sales_table():
    for item in json_raw_data["products"]:
        product_id = item["productId"]
        for subitem in item["variantList"]:
            mertchant_id = subitem["listing"]["merchantId"]
            price = subitem["listing"]["priceInfo"]["price"]
            insert_data_sales(conn, date_time, product_id, mertchant_id, price)


def entry_store_table():
    for item in json_raw_data["products"]:
        for subitem in item["variantList"]:
            mertchant_id = subitem["listing"]["merchantId"]
            mertchant_name = subitem["listing"]["merchantName"]
            insert_or_update_store_data(conn, mertchant_id, mertchant_name)


if __name__ == "__main__":
    date_time = datetime.datetime.now()
    data_download(date_time)
    read_data()

    conn = connect_to_database("database1")
    create_tables(conn)
    entry_product_table()
    entry_sales_table()
    entry_store_table()


close_connection(conn)
