
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import scipy.sparse as sparse
import numpy as np
import pandas as pd

def count_vectorizer(sequences):
    count_model = CountVectorizer(ngram_range=(1,1))
    X = count_model.fit_transform(sequences)
    return count_model, X

def normalize_cooccurrence_matrix(Xc):
    g = sparse.diags(1./Xc.diagonal())
    # normalized co-occurence matrix
    Xc_norm = g * Xc
    return Xc_norm


def concurrence_matrix(X):
    # Co-occurrence matrix in sparse csr format
    Xc = (X.T * X)
    # Normalize matrix, method in modeling.py
    Xc_norm = normalize_cooccurrence_matrix(Xc)
    # Fill same word cooccurence to 0 so we don't get it as a frequency result
    Xc.setdiag(0)
    Xc_norm.setdiag(0)

    return Xc, Xc_norm


def vectors_for_products_in_freq_matrix(vectorizer, matrix, product_names, verbose=True):
    # Returns a list of vectors asociated to each one of the products
    binary_rep_list = []
    for product_name in product_names:
        feature_index = vectorizer.vocabulary_[product_name]
        sequence_counts = [binary[0] for binary in matrix[:, feature_index:feature_index + 1]]
        binary_rep_list.append(sequence_counts)

        if verbose == True:
            print('Product encoded name: {}, \nFeature index: {}'.format(product_name, feature_index))
            print('Item frequency in product sequence: {}'.format(sequence_counts[:50]))

    return binary_rep_list


def vectors_for_products_in_cooccurrence_matrix(vectorizer, matrix, product_names, verbose=True):
    """
    Return rows of co-occurrence matrix that correspond to products passed.
    - param vectorizer: count_vectorizer model
    - param matrix: Co-ocurrence matrix
    - param product_names: Names of the products for which we want to obtain the frequency rows
    - param verbose: Defaults to true. Whether or not to print the logs
    - return binary_rep_list: Return rows of frequencey matrix that correspond to products passed.
    """
    # Returns a dictionary
    binary_rep_list = {}
    for product_name in product_names:
        feature_index = vectorizer.vocabulary_[product_name]
        sequence_counts = matrix[feature_index]
        binary_rep_list[product_name] = sequence_counts

        if verbose == True:
            print('Product encoded name: {}, \nFeature index: {}'.format(product_name, feature_index))
            print('Item frequencey in product sequence: {}'.format(sequence_counts))

    return binary_rep_list


def cooccurrent_product_frequencies(vectorizer, matrix, product_names, verbose=True):
    """
    Calculates the products that have ocurred in the same context (ordered at the same time) as queried products (product_names)
    - param vectorizer: count_vectorizer model
    - param matrix: Co-ocurrence matrix
    - param product_names: Names of the products for which we want to obtain the frequency rows
    - param verbose: Defaults to true. Whether or not to print the logs

    - return cooccurence_vectors_dict: Return rows of co-occurrence matrix that correspond to products passed.
    """
    product_occurrences_vector = vectors_for_products_in_cooccurrence_matrix(vectorizer, matrix, product_names, verbose)
    sorted_vocab = {k: v for k, v in sorted(vectorizer.vocabulary_.items(), key=lambda item: item[1])}

    cooccurence_vectors_dict = {}
    for product, occurrences_vector in product_occurrences_vector.items():
        product_occurrences_dict = {list(sorted_vocab.keys())[i]: e for i, e in enumerate(occurrences_vector) if e != 0}

        # Sort product_occurrences_dict by value descending so we know which produxts appeared more times in the same
        # context as queried products. Then store it in cooccurence_vectors with the corresponding product name as key
        sorted_ocurrences = {k: v for k, v in
                             sorted(product_occurrences_dict.items(), key=lambda item: item[1], reverse=True)}

        # Create dataframe to present data
        df_ocurrences = pd.DataFrame()
        df_ocurrences['product_name_encoded'] = list(sorted_ocurrences.keys())
        df_ocurrences['ocurrences'] = list(sorted_ocurrences.values())

        cooccurence_vectors_dict[product] = df_ocurrences
    return cooccurence_vectors_dict


def tfidf_transformer(sequence_frequencies, count_model):
    transformer = TfidfTransformer()
    transformed_weights = transformer.fit_transform(sequence_frequencies)
    weights = np.asarray(transformed_weights.mean(axis=0)).ravel().tolist()
    return pd.DataFrame({'product': count_model.get_feature_names(), 'weight': weights}).sort_values(by='weight', ascending=False)