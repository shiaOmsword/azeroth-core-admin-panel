def unpack_item_values(item_ids:str) -> dict:
    items = item_ids.split()
    item_dict = {}
    
    for index,id in enumerate(items,start=1):
        item_dict[f"item_{index}"] = id
    return item_dict
        
    