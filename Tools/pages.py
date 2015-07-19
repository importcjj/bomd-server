#coding:utf-8




def pageHandle(all_items, items_num, pageID):
    
    try:
        pageID = int(pageID)
    except:
        pageID = 1
    
    length = len(all_items)
    maxPage = length / items_num
    remainder = length % items_num
    if remainder > 0 : maxPage += 1
    
    if pageID < 1:
        pageID = 1
    elif pageID > maxPage:
        PageID = maxPage

    if pageID == maxPage and remainder:
        items = all_items[items_num * (pageID - 1) : items_num * (pageID - 1) + remainder + 1]
    else:
        items = all_items[items_num * (pageID - 1) : items_num * (pageID - 1) + items_num]
        
        
    
    
    return [maxPage, pageID, items]