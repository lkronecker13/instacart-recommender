

# Extract sequences and put them into a dictionary with user id as key and and product sequences per user as values.
def process_sequences_to_dict(df_order_products, df_orders, df_products, number_of_users=None, as_sentences=True):
    """
    Process product sequences.
    - param df_order_products: Dataframe that contains orders per product (train, prior)
    - param df_orders: Dataframe of orders prefiltered in train or prior
    - param number_of_users: Defaults to None. If (int) is passed it will process as many users as pased
    - param as_sentences: Defaults to true. If true it will process each product sequence into one string like sentence., otherwise it will
                          retirn one list dfor each sequence with each product as an entry of the list
    - return user_sequences_dict: Dictionary with user_id as keys and corresponding sequences as values.
                                (Use to know which sequences belong to whhat user)
    - return all_sequences: List of all sequences concatenated together.
    """
    user_sequences_dict = {}
    all_sequences = []
    user_count = 0
    df_order_products_group_userid = df_order_products.merge(df_orders, how='left', on='order_id').groupby(['user_id'])
    for user_id, group in df_order_products_group_userid:
        product_sequences = []
        for order_id in group['order_id'].unique():
            extracted_sequence = create_product_sequence_for_orderid(group, df_products, order_id, as_sentences)
            product_sequences.append(extracted_sequence)
            user_count += 1

        # Set the extracted sequences to the corresponding user id
        user_sequences_dict[user_id] = product_sequences[0]
        # Concatenate all sequences together
        all_sequences.append(product_sequences[0])

        # If target number of users has been reached then break the loop
        if user_count == number_of_users:
            break
    return user_sequences_dict, all_sequences



def create_product_sequence_for_orderid(dataframe_slice, df_products, order_id, as_sentences=True):
    tmp_dataframe_slice = dataframe_slice.merge(df_products, how='left', on='product_id')
    # Extract sequences for a specific order
    sequence = tmp_dataframe_slice.loc[tmp_dataframe_slice['order_id']==order_id].sort_values(by=['add_to_cart_order'], ascending=True)['product_name_encoded'].values
    if as_sentences == True:
        sequence = ' '.join(sequence)
    return sequence


def extract_orders_from_slice(df_slice, df_products, df_order_products_prior, as_sentences=False):
    df_slice_tmp = df_slice.reset_index().merge(df_order_products_prior, on='order_id', how='left')
    all_sequences = []
    for order_id in df_slice_tmp['order_id'].unique():
        extracted_sequence = create_product_sequence_for_orderid(df_slice_tmp, df_products, order_id, as_sentences)
        # Concatenate all sequences together
        all_sequences.append(extracted_sequence)
    return all_sequences

