from data_cleaning import *

#first making copy of product table and categorize products

product_category_df = products_cl.copy()


product_category_df["category"] = ""

product_category_df.loc[product_category_df["desc"].str.contains("keyboard", case=False), "category"] += ", keyboard"
product_category_df.loc[product_category_df["name"].str.contains("^.{0,7}apple iphone", case=False), "category"] += ", smartphone"
product_category_df.loc[product_category_df["name"].str.contains("^.{0,7}apple ipod", case=False), "category"] += ", ipod"
product_category_df.loc[product_category_df["name"].str.contains("^.{0,7}apple ipad|tablet", case=False), "category"] += ", tablet"
product_category_df.loc[product_category_df["name"].str.contains("imac|mac mini|mac pro", case=False), "category"] += ", desktop"
product_category_df.loc[product_category_df["name"].str.contains("macbook", case=False), "category"] += ", laptop"
product_category_df.loc[product_category_df["desc"].str.contains("backpack", case=False), "category"] += ", backpack"
product_category_df.loc[product_category_df["desc"].str.contains("case|funda|housing|casing|folder", case=False), "category"] += ", case"
product_category_df.loc[product_category_df["desc"].str.contains("dock|hub|connection|expansion box", case=False), "category"] += ", dock"
product_category_df.loc[product_category_df["desc"].str.contains("cable|connector|lightning to usb|wall socket|power strip", case=False), "category"] += ", cable"
product_category_df.loc[product_category_df["desc"].str.contains("flash drive|hard drive|pendrive|hard disk|memory|storage|^ssd|^hardssd|modules|ssd expansion", case=False), "category"] = ", storage"
product_category_df.loc[product_category_df["desc"].str.contains("battery", case=False), "category"] += ", battery"
product_category_df.loc[product_category_df["desc"].str.contains("headset|headphones", case=False), "category"] += ", headset"
product_category_df.loc[product_category_df["desc"].str.contains("charger", case=False), "category"] += ", charger"
product_category_df.loc[product_category_df["desc"].str.contains("mouse|trackpad", case=False), "category"] += ", mouse"
product_category_df.loc[product_category_df["desc"].str.contains("stand|support", case=False), "category"] += ", stand"
product_category_df.loc[product_category_df["desc"].str.contains("strap|armband|belt|bracelet", case=False), "category"] += ", strap"
product_category_df.loc[product_category_df["desc"].str.contains("^.{0,6}apple watch|smartwatch|smart watch", case=False), "category"] += ", smartwatch"
product_category_df.loc[product_category_df["desc"].str.contains("adapter", case=False), "category"] += ", adapter"
product_category_df.loc[product_category_df["desc"].str.contains("^.{0,7}ram", case=False), "category"] += ", ram"
product_category_df.loc[product_category_df["desc"].str.contains("protect|cover|sleeve|screensaver|shell", case=False), "category"] += ", protection"
product_category_df.loc[product_category_df["desc"].str.contains("nas|server|raid|synology", case=False), "category"] += ", server"
product_category_df.loc[product_category_df["desc"].str.contains("scale", case=False), "category"] += ", scale"
product_category_df.loc[product_category_df["desc"].str.contains("thermometer", case=False), "category"] += ", thermometer"
product_category_df.loc[product_category_df["desc"].str.contains("monitor", case=False), "category"] += ", monitor"
product_category_df.loc[product_category_df["desc"].str.contains("speaker|music system", case=False), "category"] += ", speaker"
product_category_df.loc[product_category_df["desc"].str.contains("camera", case=False), "category"] += ", camera"
product_category_df.loc[product_category_df["desc"].str.contains("pointer", case=False), "category"] += ", pointer"
product_category_df.loc[product_category_df["desc"].str.contains("refurbished|reconditioned|like new", case=False), "category"] += ", refurbished"

product_category_df.loc[product_category_df["category"] == "", "category"] += ", other"

product_category_df["category"] = product_category_df["category"].str[2:]
