from src.preprocessing.preprocess import Preprocess

if __name__ == '__main__':
    try:
        data_collection = Preprocess()
        data_collection.main()
    except Exception as e:
        raise e
