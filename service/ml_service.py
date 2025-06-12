import tensorflow as tf
import os
import tf_keras as k3
import numpy as np
from sqlalchemy.orm import Session
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
        print(predictions)
        predicted_class = np.argmax(predictions)
        return risk_order[predicted_class]
        
    @classmethod     
    def articleRecommendation(cls, input_data=None, top_n=5, article_limit=5):
        
        project_root = os.path.dirname(os.path.dirname(__file__))
        model_path = os.path.join(project_root, "model_rekomendasi_artikel")
        
        # Load model 
        model = k3.models.load_model(model_path)
        
        
        # Load data artikel
        try:
            df_artikel = pd.read_csv(os.path.join(project_root, "data_artikel_new.csv"))
        except:
            print("⚠️  File data_artikel_new.csv tidak ditemukan, menggunakan data simulasi")
            df_artikel = cls._create_sample_article_data()
        
        # Data input pengguna (gunakan default jika tidak ada input)
        if input_data is None:
            contoh_1 = np.array([[
                120,  # tekanan_sistolik: Normal (120 mmHg)
                80,   # tekanan_diastolik: Normal (80 mmHg) 
                90,   # gula_darah: Normal (90 mg/dL)
                36.8, # suhu_tubuh: Normal (36.8°C)
                2,    # trimester: Trimester kedua
                75,   # denyut_jantung: Normal (75 bpm)
                0,    # demam_lebih_2_hari: Tidak ada demam
                0,    # pusing: Tidak pusing
                0,    # sulit_tidur: Tidak sulit tidur
                0,    # nyeri_perut_berat: Tidak ada nyeri perut berat
                0     # diare_berulang: Tidak ada diare berulang
            ]])
        else:
            contoh_1 = input_data.reshape(1, -1) if input_data.ndim == 1 else input_data
        
        # Preprocessing jika scaler tersedia
        if scaler is not None:
            contoh_1_scaled = scaler.transform(contoh_1)
        else:
            contoh_1_scaled = contoh_1
        
        # Prediksi menggunakan model
        predicted_probs = model.predict(contoh_1_scaled)[0]
        
        # Label kondisi (sesuaikan dengan model Anda)
        if mlb is not None:
            kondisi_labels = mlb.classes_
        else:
            kondisi_labels = [
                'normal', 'prehipertensi', 'hipertensi_ringan', 'hipertensi_berat',
                'gula_darah_tinggi', 'gula_darah_rendah', 'bradikardia', 'takikardia',
                'demam_lebih_2_hari', 'pusing', 'sulit_tidur', 'nyeri_perut_berat', 'diare_berulang'
            ]
        
        # Ambil top-N kondisi dengan probabilitas tertinggi
        top_indices = np.argsort(predicted_probs)[::-1][:top_n]
        
        # Filter kondisi dengan probabilitas > threshold (misal 0.1 atau 10%)
        threshold = 0.1
        significant_conditions = []
        
        print("=" * 70)
        print("🏥 HASIL ANALISIS KESEHATAN & REKOMENDASI ARTIKEL")
        print("=" * 70)
        
        # Tampilkan input data
        cls._display_input_summary(contoh_1[0])
        
        print(f"🔍 KONDISI KESEHATAN YANG TERDETEKSI (Probabilitas > {threshold*100}%):")
        print("-" * 50)
        
        for i, idx in enumerate(top_indices, 1):
            if idx < len(kondisi_labels) and predicted_probs[idx] > threshold:
                kondisi = kondisi_labels[idx]
                probabilitas = predicted_probs[idx] * 100
                
                penjelasan = cls._get_kondisi_explanation(kondisi)
                
                print(f"{i}. {penjelasan['nama']}")
                print(f"   Probabilitas: {probabilitas:.1f}%")
                print(f"   Deskripsi: {penjelasan['deskripsi']}")
                print(f"   Rekomendasi: {penjelasan['rekomendasi']}")
                print()
                
                significant_conditions.append({
                    'rank': i,
                    'kondisi': kondisi,
                    'nama_kondisi': penjelasan['nama'],
                    'probabilitas': probabilitas,
                    'probabilitas_str': f"{probabilitas:.1f}%",
                    'deskripsi': penjelasan['deskripsi'],
                    'rekomendasi': penjelasan['rekomendasi']
                })
        
        # Jika tidak ada kondisi signifikan, ambil yang probabilitas tertinggi
        if not significant_conditions:
            idx = top_indices[0]
            kondisi = kondisi_labels[idx] if idx < len(kondisi_labels) else 'unknown'
            probabilitas = predicted_probs[idx] * 100
            penjelasan = cls._get_kondisi_explanation(kondisi)
            
            significant_conditions.append({
                'rank': 1,
                'kondisi': kondisi,
                'nama_kondisi': penjelasan['nama'],
                'probabilitas': probabilitas,
                'probabilitas_str': f"{probabilitas:.1f}%",
                'deskripsi': penjelasan['deskripsi'],
                'rekomendasi': penjelasan['rekomendasi']
            })
        
        # Ambil tags dari kondisi yang terdeteksi
        detected_tags = [cond['kondisi'] for cond in significant_conditions]
        
        # Cari artikel yang relevan
        recommended_articles = cls._get_relevant_articles(detected_tags, df_artikel, article_limit)
        
        # Tampilkan rekomendasi artikel
        print("📚 REKOMENDASI ARTIKEL BERDASARKAN KONDISI ANDA:")
        print("-" * 50)
        
        if recommended_articles.empty:
            print("❌ Tidak ada artikel yang relevan ditemukan.")
            print("💡 Silakan konsultasi dengan tenaga kesehatan untuk informasi lebih lanjut.")
        else:
            for i, (_, artikel) in enumerate(recommended_articles.iterrows(), 1):
                print(f"{i}. 📖 {artikel['judul']}")
                print(f"   Kategori: {artikel['kategori']}")
                print(f"   Deskripsi: {artikel['deskripsi']}")
                
                # Tampilkan relevansi dengan kondisi
                matching_tags = [tag for tag in detected_tags if tag in artikel['tag']]
                if matching_tags:
                    print(f"   Relevan untuk: {', '.join(matching_tags)}")
                
                print(f"   Tags: {artikel['tag']}")
                print()
        
        print("=" * 70)
        print("💡 CATATAN PENTING:")
        print("   • Hasil ini adalah prediksi berdasarkan data yang diinput")
        print("   • Selalu konsultasikan kondisi kesehatan dengan tenaga medis")
        print("   • Artikel yang direkomendasikan bersifat informatif dan edukatif")
        print("=" * 70)
        
        return {
            'input_data': contoh_1[0].tolist(),
            'kondisi_terdeteksi': significant_conditions,
            'artikel_rekomendasi': recommended_articles.to_dict('records') if not recommended_articles.empty else [],
            'summary': cls._generate_summary(significant_conditions, len(recommended_articles)),
            'raw_probabilities': {
                kondisi_labels[i]: f"{prob*100:.2f}%" 
                for i, prob in enumerate(predicted_probs) 
                if i < len(kondisi_labels)
            }
        }
    
    @staticmethod
    def _display_input_summary(input_data):
        """Menampilkan ringkasan data input"""
        print(f"📊 DATA KESEHATAN YANG DIANALISIS:")
        print(f"   • Tekanan Darah: {input_data[0]:.0f}/{input_data[1]:.0f} mmHg")
        print(f"   • Gula Darah: {input_data[2]:.0f} mg/dL")
        print(f"   • Suhu Tubuh: {input_data[3]:.1f}°C")
        print(f"   • Trimester: {input_data[4]:.0f}")
        print(f"   • Denyut Jantung: {input_data[5]:.0f} bpm")
        
        gejala = ['Demam >2 hari', 'Pusing', 'Sulit Tidur', 'Nyeri Perut Berat', 'Diare Berulang']
        gejala_ada = [gejala[i] for i in range(5) if input_data[6+i] == 1]
        
        if gejala_ada:
            print(f"   • Gejala yang Dialami: {', '.join(gejala_ada)}")
        else:
            print(f"   • Gejala Tambahan: Tidak ada")
        print()
    
    @staticmethod
    def _get_relevant_articles(tags, df_artikel, limit=5):
        """Mencari artikel yang relevan berdasarkan tags kondisi"""
        if df_artikel.empty:
            return pd.DataFrame()
        
        # Filter artikel yang mengandung tag yang sesuai
        mask = df_artikel['tag'].apply(
            lambda x: any(tag in str(x).split('|') for tag in tags)
        )
        
        relevant_articles = df_artikel[mask].head(limit)
        
        # Jika tidak ada yang cocok, ambil artikel umum atau random
        if relevant_articles.empty:
            relevant_articles = df_artikel.head(limit)
        
        return relevant_articles[['judul', 'kategori', 'deskripsi', 'tag']]
    
    @staticmethod
    def _create_sample_article_data():
        """Membuat data artikel sampel berdasarkan format yang diberikan"""
        sample_data = [
            {
                'judul': 'Mengatasi Rasa Lelah yang Tak Tertahankan',
                'kategori': 'Kesehatan Ibu Hamil',
                'deskripsi': 'Strategi mengelola fatigue ekstrim selama kehamilan.',
                'tag': 'bradikardia|gula_darah_rendah'
            },
            {
                'judul': 'Panduan Menjaga Tekanan Darah Normal Selama Kehamilan',
                'kategori': 'Kesehatan Kardiovaskular',
                'deskripsi': 'Tips mencegah dan mengelola hipertensi pada ibu hamil.',
                'tag': 'hipertensi_ringan|hipertensi_berat|prehipertensi'
            },
            {
                'judul': 'Mengelola Gula Darah untuk Kehamilan Sehat',
                'kategori': 'Diabetes Gestasional',
                'deskripsi': 'Panduan lengkap mengatasi masalah gula darah saat hamil.',
                'tag': 'gula_darah_tinggi|gula_darah_rendah'
            },
            {
                'judul': 'Mengenali dan Mengatasi Gejala Kehamilan yang Mengkhawatirkan',
                'kategori': 'Tanda Bahaya Kehamilan',
                'deskripsi': 'Cara mengenali gejala yang memerlukan perhatian medis segera.',
                'tag': 'demam_lebih_2_hari|pusing|nyeri_perut_berat|diare_berulang'
            },
            {
                'judul': 'Tips Tidur Berkualitas untuk Ibu Hamil',
                'kategori': 'Kesehatan Mental',
                'deskripsi': 'Solusi mengatasi gangguan tidur selama kehamilan.',
                'tag': 'sulit_tidur|normal'
            }
        ]
        
        return pd.DataFrame(sample_data)
    
    @staticmethod
    def _get_kondisi_explanation(kondisi):
        """Mapping kondisi ke penjelasan yang mudah dipahami"""
        explanations = {
            'normal': {
                'nama': '✅ Kondisi Normal',
                'deskripsi': 'Semua parameter kesehatan dalam batas normal.',
                'rekomendasi': 'Pertahankan pola hidup sehat dan rutin kontrol kehamilan.'
            },
            'prehipertensi': {
                'nama': '⚠️ Prehipertensi', 
                'deskripsi': 'Tekanan darah sedikit di atas normal, berisiko hipertensi.',
                'rekomendasi': 'Kurangi asupan garam, tingkatkan aktivitas fisik ringan.'
            },
            'hipertensi_ringan': {
                'nama': '🔶 Hipertensi Ringan',
                'deskripsi': 'Tekanan darah tinggi tingkat ringan yang perlu diawasi.',
                'rekomendasi': 'Konsultasi dokter, pantau tekanan darah rutin.'
            },
            'hipertensi_berat': {
                'nama': '🔴 Hipertensi Berat',
                'deskripsi': 'Tekanan darah tinggi yang memerlukan perhatian medis segera.',
                'rekomendasi': 'Segera konsultasi dokter spesialis kandungan.'
            },
            'gula_darah_tinggi': {
                'nama': '🍯 Gula Darah Tinggi',
                'deskripsi': 'Kadar gula darah di atas normal, risiko diabetes gestasional.',
                'rekomendasi': 'Kontrol asupan karbohidrat, cek gula darah rutin.'
            },
            'gula_darah_rendah': {
                'nama': '⬇️ Gula Darah Rendah',
                'deskripsi': 'Kadar gula darah di bawah normal (hipoglikemia).',
                'rekomendasi': 'Makan teratur, bawa camilan sehat.'
            },
            'bradikardia': {
                'nama': '💓 Denyut Jantung Lambat',
                'deskripsi': 'Denyut jantung di bawah normal (< 60 bpm).',
                'rekomendasi': 'Konsultasi dokter untuk evaluasi kondisi jantung.'
            },
            'takikardia': {
                'nama': '💗 Denyut Jantung Cepat',
                'deskripsi': 'Denyut jantung di atas normal (> 100 bpm).',
                'rekomendasi': 'Istirahat cukup, hindari stres berlebihan.'
            },
            'demam_lebih_2_hari': {
                'nama': '🌡️ Demam Berkepanjangan',
                'deskripsi': 'Demam yang berlangsung lebih dari 2 hari.',
                'rekomendasi': 'Segera konsultasi dokter untuk penanganan.'
            },
            'pusing': {
                'nama': '😵 Pusing',
                'deskripsi': 'Mengalami gejala pusing atau vertigo.',
                'rekomendasi': 'Istirahat, hindari perubahan posisi mendadak.'
            },
            'sulit_tidur': {
                'nama': '😴 Sulit Tidur',
                'deskripsi': 'Mengalami gangguan tidur atau insomnia.',
                'rekomendasi': 'Ciptakan rutinitas tidur yang nyaman.'
            },
            'nyeri_perut_berat': {
                'nama': '🤰 Nyeri Perut Berat',
                'deskripsi': 'Mengalami nyeri perut yang signifikan.',
                'rekomendasi': 'Segera konsultasi dokter kandungan.'
            },
            'diare_berulang': {
                'nama': '🚽 Diare Berulang',
                'deskripsi': 'Mengalami diare yang berlangsung berulang.',
                'rekomendasi': 'Jaga hidrasi, konsultasi dokter jika berkepanjangan.'
            }
        }
        
        return explanations.get(kondisi, {
            'nama': f'❓ {kondisi.replace("_", " ").title()}',
            'deskripsi': 'Kondisi yang perlu evaluasi lebih lanjut.',
            'rekomendasi': 'Konsultasi dengan tenaga kesehatan.'
        })
    
    @staticmethod
    def _generate_summary(conditions, article_count):
        """Generate ringkasan hasil analisis"""
        if not conditions:
            return "Tidak ada kondisi signifikan yang terdeteksi."
        
        main_condition = conditions[0]
        summary = f"Kondisi utama yang terdeteksi: {main_condition['nama_kondisi']} "
        summary += f"dengan tingkat keyakinan {main_condition['probabilitas_str']}. "
        
        if article_count > 0:
            summary += f"Ditemukan {article_count} artikel yang relevan untuk kondisi Anda."
        else:
            summary += "Tidak ditemukan artikel yang spesifik untuk kondisi ini."
        
        return summary
    

# recommender = MLService()
# recommender.maternalClassification()