import tensorflow as tf
import os
import tf_keras as k3
import numpy as np
import pandas as pd

class MLService:
    
    @staticmethod
    def maternalClassification(inputData):
        risk_order = ["low risk", "mid risk", "high risk"]
        project_root = os.path.dirname(os.path.dirname(__file__))
        model_path = os.path.join(project_root, "model_klasifikasi_maternal")

        model = k3.models.load_model(model_path)
        input_data = np.array([inputData])
        
        predictions = model.predict(input_data)
        predicted_class = np.argmax(predictions)
        return risk_order[predicted_class]
        
        
    @classmethod     
    def articleRecommendation(cls, input_data=None, article_limit=None):
        """
        Returns collection of articles from the model's knowledge base
        
        Args:
            input_data: Health data array [11 features] (optional for filtering)
            article_limit: Maximum number of articles to return (None for all)
        
        Returns:
            list: Collection of articles from the model
        """
        try:
            # Load articles data that the model uses
            articles_df = cls._load_articles_data()
            
            if articles_df.empty:
                return []
            
            # Apply limit if specified
            if article_limit:
                articles_df = articles_df.head(article_limit)
            
            # Convert to clean format
            articles_collection = []
            for _, row in articles_df.iterrows():
                article = {
                    'id': int(row['id']) if 'id' in row else None,
                    'title': row['judul'],
                    'category': row['kategori'],
                    'description': row['deskripsi'],
                    'tags': row['tag'].split('|') if isinstance(row['tag'], str) else []
                }
                articles_collection.append(article)
            
            return articles_collection
            
        except Exception as e:
            print(f"Error loading articles: {str(e)}")
            return []
    
    @classmethod
    def getAllArticles(cls):
        """Get all articles from the model's knowledge base"""
        return cls.articleRecommendation()
    
    @classmethod
    def getArticlesByCategory(cls, category):
        """Get articles filtered by category"""
        all_articles = cls.articleRecommendation()
        return [article for article in all_articles if article['category'].lower() == category.lower()]
    
    @classmethod
    def getArticlesByTag(cls, tag):
        """Get articles filtered by specific tag"""
        all_articles = cls.articleRecommendation()
        return [article for article in all_articles if tag in article['tags']]
    
    @staticmethod
    def _load_articles_data():
        """Load articles data from CSV or return sample data"""
        try:
            project_root = os.path.dirname(os.path.dirname(__file__))
            return pd.read_csv(os.path.join(project_root, "data_artikel_new.csv"))
        except:
            return MLService._create_sample_articles_dataframe()
    
    @staticmethod
    def _create_sample_articles_dataframe():
        """Create sample articles data"""
        sample_data = [
            {
                'id': 1,
                'judul': 'Mengatasi Rasa Lelah yang Tak Tertahankan',
                'kategori': 'Kesehatan Ibu Hamil',
                'deskripsi': 'Strategi mengelola fatigue ekstrim selama kehamilan.',
                'tag': 'bradikardia|gula_darah_rendah'
            },
            {
                'id': 2,
                'judul': 'Panduan Menjaga Tekanan Darah Normal Selama Kehamilan',
                'kategori': 'Kesehatan Kardiovaskular',
                'deskripsi': 'Tips mencegah dan mengelola hipertensi pada ibu hamil.',
                'tag': 'hipertensi_ringan|hipertensi_berat|prehipertensi'
            },
            {
                'id': 3,
                'judul': 'Mengelola Gula Darah untuk Kehamilan Sehat',
                'kategori': 'Diabetes Gestasional',
                'deskripsi': 'Panduan lengkap mengatasi masalah gula darah saat hamil.',
                'tag': 'gula_darah_tinggi|gula_darah_rendah'
            },
            {
                'id': 4,
                'judul': 'Mengenali dan Mengatasi Gejala Kehamilan yang Mengkhawatirkan',
                'kategori': 'Tanda Bahaya Kehamilan',
                'deskripsi': 'Cara mengenali gejala yang memerlukan perhatian medis segera.',
                'tag': 'demam_lebih_2_hari|pusing|nyeri_perut_berat|diare_berulang'
            },
            {
                'id': 5,
                'judul': 'Tips Tidur Berkualitas untuk Ibu Hamil',
                'kategori': 'Kesehatan Mental',
                'deskripsi': 'Solusi mengatasi gangguan tidur selama kehamilan.',
                'tag': 'sulit_tidur|normal'
            }
        ]
        return pd.DataFrame(sample_data)
    
    @staticmethod
    def _get_condition_name(condition):
        """Get human-readable condition names"""
        condition_names = {
            'normal': 'Kondisi Normal',
            'prehipertensi': 'Prehipertensi',
            'hipertensi_ringan': 'Hipertensi Ringan',
            'hipertensi_berat': 'Hipertensi Berat',
            'gula_darah_tinggi': 'Gula Darah Tinggi',
            'gula_darah_rendah': 'Gula Darah Rendah',
            'bradikardia': 'Denyut Jantung Lambat',
            'takikardia': 'Denyut Jantung Cepat',
            'demam_lebih_2_hari': 'Demam Berkepanjangan',
            'pusing': 'Pusing',
            'sulit_tidur': 'Sulit Tidur',
            'nyeri_perut_berat': 'Nyeri Perut Berat',
            'diare_berulang': 'Diare Berulang'
        }
        return condition_names.get(condition, condition.replace('_', ' ').title())
