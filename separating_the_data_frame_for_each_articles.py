def separating_the_data_frame_for_each_articles(df,all_details,final_all_indexing):
    # print(df)
    # print(all_details)
    my_dict = {}

    for i in range(len(all_details)):
        # print(a)
        # print(list(a[1:]))
        a=all_details[i]
        index_list = a[1:]
        dfp=df[df.index.isin(index_list)]
        # print(dfp)
        # for i in range(len(all_details)):
        my_dict[a[0]] = dfp.to_dict('dict')
    return my_dict
