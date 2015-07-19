#coding:utf-8




def pageHandle(all_items, items_num, pageID):
    
    try:
        pageID = int(pageID)
    except:
        pageID = 1
    
    length = len(all_items)
    (maxPage, remainder)= divmod(length, items_num)
    if remainder > 0 : maxPage += 1
    
    if pageID < 1 : pageID = 1
    if pageID > maxPage : PageID = maxPage

    start_index = items_num*(pageID-1)
    if pageID == maxPage and remainder:
        items = all_items[start_index : start_index + remainder + 1]
    else:
        items = all_items[start_index : start_index + items_num]

    return (maxPage, pageID, items)