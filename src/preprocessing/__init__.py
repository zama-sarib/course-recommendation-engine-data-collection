from from_root import from_root
from src.exception import CustomException
from src.logger import logging
import os, sys
import pandas as pd
import subprocess
from zipfile import ZipFile
import shutil

class Preprocess():
    def __init__(self):
        self.dataset_path = os.path.join(os.getcwd(),'Dataset')

    def unzip_data(self,path):
        try:
            
            logging.info(f"-------------------------Extracting Data--------------------------------------")
            for file in os.listdir(path):
                logging.info(f"Extracting {file} ...")
                zip_file_path = os.path.join(path,file)
                unzip_file_path = zip_file_path.replace(".zip","")
                with ZipFile(zip_file_path, 'r') as files:
                    files.extractall(path=unzip_file_path)
                
                files.close()
                os.remove(zip_file_path)
            logging.info("-------------------------Process Completed---------------------------------------")

        except Exception as e:
            message = CustomException(e, sys)
            return {"File Extracted": False, "Reason": message.error_message}
        
    
    def read_data(self,path: str) -> pd.DataFrame:

        try:
            logging.info("Reading file(s) from: {path}")
            final_df = pd.DataFrame()
            for file in os.listdir(path):
                file_path = os.path.join(path,file)
                temp_df = pd.read_csv(file_path)
                final_df = pd.concat([final_df,temp_df],axis=0,ignore_index=True)
                logging.info("Completed Reading files from: {file_path}")
            return final_df
        except Exception as e:
            message = CustomException(e,sys)
            return {"File read": False, "Reason": message.error_message}
        
        
    def save_data(self,dataframe: pd.DataFrame, path: str):
        try:
            logging.info("Saving final dataframe to csv")
            final_path = os.path.join(path,"final.csv")
            dataframe.to_csv(final_path,index=False)
            logging.info("Saving Completed")
        except Exception as e:
            message = CustomException(e,sys)
            return {"Save Data": False, "Reason":message.error_message}
        
    
    def transformation_one(self,path)->pd.DataFrame:
        try:
            logging.info(f"Transformation one for dataframe: {path} has started")
            df1 = pd.DataFrame()
            for file in os.listdir(path):
                complete_file_path = os.path.join(path,file)
                temp_df = pd.read_csv(complete_file_path)
                df1 = pd.concat([df1,temp_df],axis=0,ignore_index=True)

            #columns = ['id','title','url','is_paid','num_subscribers','avg_rating','num_reviews','published_time','price_detail__amount']
            columns = ['course_id','course_title','url','num_subscribers','Rating','num_reviews','published_timestamp','price']
            #column_rename = {'id':'course_id','title':'course_title','url':'url','num_subscribers':'num_subscribers','avg_rating':'Rating','num_reviews':'num_reviews','published_time':'published_timestamp','price_detail__amount':'price'}
            df1 = df1[columns]
            df1.drop_duplicates(subset=['course_id'],keep='first',inplace=True)
            logging.info(f"Transformation one for dataframe: {path} has completed")
            return df1
        except Exception as e:
            message = CustomException(e,sys)
            return {"Transformation one Completed": False, "Reason":message.error_message}
        

    def transformation_two(self,path)->pd.DataFrame:
        try:
            logging.info(f"Transformation Two for dataframe: {path} has started")
            df2 = pd.DataFrame()
            for file in os.listdir(path):
                complete_file_path = os.path.join(path,file)
                temp_df = pd.read_csv(complete_file_path)
                df2 = pd.concat([df2,temp_df],axis=0,ignore_index=True)

            columns = ['course_id','course_title','url','num_subscribers','Rating','num_reviews','published_timestamp','price']
            df2.drop_duplicates(subset=['id'],keep='first',inplace=True)
            #columns = ['id','title','url','num_subscribers','avg_rating','num_reviews','published_time','price_detail__amount']
            column_rename = {'id':'course_id','title':'course_title','url':'url','num_subscribers':'num_subscribers','avg_rating':'Rating','num_reviews':'num_reviews','published_time':'published_timestamp','price_detail__amount':'price'}
            df2.rename(columns=column_rename,inplace=True)
            df2 = df2[columns]
            logging.info(f"Transformation Two for dataframe: {path} has completed")
            return df2
        except Exception as e:
            message = CustomException(e,sys)
            return {"Transformation two Completed": False, "Reason":message.error_message}
        

    def transformation_three(self,path)->pd.DataFrame:
        try:
            logging.info(f"Transformation Three for dataframe: {path} has started")
            df3 = pd.DataFrame()
            for file in os.listdir(path):
                complete_file_path = os.path.join(path,file)
                temp_df = pd.read_csv(complete_file_path)
                df3 = pd.concat([df3,temp_df],axis=0,ignore_index=True)

            #columns = ['id','title','url','is_paid','num_subscribers','avg_rating','num_reviews','published_time','price_detail__amount']
            columns = ['course_id','course_title','url','num_subscribers','num_reviews','published_timestamp','price']
            column_rename = {'course_id':'course_id','course_title':'course_title','url':'url','num_subscribers':'num_subscribers','avg_rating':'Rating','num_reviews':'num_reviews','published_timestamp':'published_timestamp','price':'price'}
            df3.rename(columns=column_rename,inplace=True)
            df3 = df3[columns]
            df3.drop_duplicates(subset=['course_id'],keep='first',inplace=True)
            logging.info(f"Transformation Three for dataframe: {path} has completed")
            return df3
        except Exception as e:
            message = CustomException(e,sys)
            return {"Transformation three Completed": False, "Reason":message.error_message}
        
    
    def remove_unnecessary_folder(self,path):
        try:
            logging.info("Delete extracted folder")
            for file in os.listdir(path):
                file_path = os.path.join(path,file)
                if not os.path.isfile(file_path):
                    logging.info(f"Deleting - {file} ...")
                    shutil.rmtree(file_path)

        except Exception as e:
            message = CustomException(e,sys)
            return {"Files Deleted": False,"Reason":message.error_message}
        


if __name__ == '__main__':
    try:
        print("----------------------------------Data Collection started ----------------------------------------------")
        
        logging.info("-----------------------------Downloading Data ---------------------------------------")
        subprocess.run(["sh", "./scripts/script.sh"]) # Download the data.
        logging.info('-----------------------------Download Completed --------------------------------------')
        preprocess = Preprocess()
        preprocess.unzip_data(preprocess.dataset_path) 
        for folder in os.listdir(preprocess.dataset_path):
            complete_file_path = os.path.join(preprocess.dataset_path,folder)
            if 'revenue' in complete_file_path:
                df1 = preprocess.transformation_one(complete_file_path)
            elif 'finance' in complete_file_path:
                df2 = preprocess.transformation_two(complete_file_path)
            else:
                df3 = preprocess.transformation_three(complete_file_path)
                
        final_df = pd.concat([df1,df2,df3],axis=0,ignore_index=True)
        preprocess.save_data(final_df,preprocess.dataset_path)
        logging.info(f"Final Data saved to {preprocess.dataset_path}")
        preprocess.remove_unnecessary_folder(preprocess.dataset_path)

        print("-------------------------------------Data Collection Completed----------------------------------------")
    except Exception as e:
        raise CustomException(e,sys)
        
        
