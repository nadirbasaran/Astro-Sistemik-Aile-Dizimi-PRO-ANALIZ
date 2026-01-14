import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Sayfa Ayarları
st.set_page_config(page_title="Astro-Sistemik Dizim", page_icon="🔮")

st.title("🔮 Astro-Sistemik Aile Dizimi Haritası")
st.markdown("Astroloji haritanız ve Aile hikayeniz birleşiyor...")

# --- KENAR ÇUBUĞU (VERİ GİRİŞİ) ---
with st.sidebar:
    st.header("1. Kişisel Bilgiler")
    cinsiyet = st.selectbox("Cinsiyetiniz", ["Erkek", "Kadın"])
    
    st.header("2. Astroloji Verileri")
    
    # SATÜRN
    st.markdown("---")
    st.write("🪐 **Satürn (Baba/Karma)**")
    saturn_ev = st.number_input("Satürn Kaçıncı Evde?", min_value=1, max_value=12, value=1)
    saturn_burc = st.selectbox("Satürn Burcu", ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"])
    
    # AY (GÜNCELLENDİ: Ev Sorusu Eklendi)
    st.markdown("---")
    st.write("🌙 **Ay (Anne/Duygular)**")
    ay_ev = st.number_input("Ay (Moon) Kaçıncı Evde?", min_value=1, max_value=12, value=1)
    ay_burc = st.selectbox("Ay (Moon) Burcu", ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"])
    
    # Açı Sorusu
    ay_aci = st.checkbox(
        "Ay, Satürn veya Plüton'dan sert açı alıyor mu?",
        help="📌 **İpucu:** Haritanızda Ay ile Satürn/Plüton arasında Kare (90°), Karşıt (180°) veya Kavuşum (0°) varsa işaretleyin."
    )
    
    # 12. EV (GÜNCELLENDİ: Başka Gezegen Sorusu)
    st.markdown("---")
    st.write("👻 **12. Ev (Sırlar ve Dışlanmışlar)**")
    st.info("Haritanızda 12. Evde bulunan gezegenleri seçiniz.")
    gezegenler_12 = st.multiselect(
        "12. Evinizde Hangi Gezegenler Var?",
        ["Yok/Boş", "Güneş", "Ay", "Merkür", "Venüs", "Mars", "Jüpiter", "Satürn", "Plüton", "Uranüs", "Neptün", "Chiron"],
        help="12. Evdeki gezegen, ailede 'kimin' veya 'neyin' saklandığını gösterir."
    )

    st.markdown("---")
    hesapla = st.button("Haritayı ve Reçeteyi Oluştur")

# --- HARİTA VE REÇETE FONKSİYONU ---
def analiz_et():
    # 1. GRAFİK KURULUMU
    G = nx.DiGraph()
    coords = {
        "Karma/Atalar": (0, 4), "BABA": (-1, 2), "ANNE": (1, 2),
        "DANIŞAN": (0, 0), "Dışlanmış Kişi": (2, -1)
    }
    
    # Düğümler
    G.add_node("Karma/Atalar", shape='s', color='#A9A9A9', pos=coords["Karma/Atalar"])
    G.add_node("BABA", shape='s', color='#87CEFA', pos=coords["BABA"])
    G.add_node("ANNE", shape='o', color='#FFB6C1', pos=coords["ANNE"])
    
    danisan_renk = '#87CEFA' if cinsiyet == "Erkek" else '#FFB6C1'
    danisan_sekil = 's' if cinsiyet == "Erkek" else 'o'
    G.add_node("DANIŞAN", shape=danisan_sekil, color=danisan_renk, pos=coords["DANIŞAN"])

    edge_colors = []
    edge_styles = []
    edge_labels = {}
    oneriler = []

    # --- MANTIK MOTORU ---

    # 1. SATÜRN (Baba Karması)
    if saturn_ev in [4, 8, 12] or saturn_burc in ['Oğlak', 'Akrep', 'Koç']:
        G.add_edge("Karma/Atalar", "BABA", color='red')
        edge_colors.append('red'); edge_styles.append('dashed')
        
        sorun = "AĞIR YÜK"
        if saturn_ev == 4: 
            sorun = "KÖK TRAVMASI"
            oneriler.append("🏠 **Satürn 4. Ev:** Baba köklerinde yerleşme sorunu veya göç travması var. Evinizde atalar için bir köşe hazırlayın.")
        if saturn_ev == 8: 
            sorun = "MİRAS/ÖLÜM"
            oneriler.append("💸 **Satürn 8. Ev:** Ailede iflas, miras kavgası veya erken ölüm korkusu var. Bedel ödemek için sadaka verin.")
        if saturn_ev == 12: 
            sorun = "GİZLİ KAYIP"
            oneriler.append("🕯️ **Satürn 12. Ev:** Baba tarafında hapis, hastane veya gizli tutulan bir utanç olabilir. Yargılamadan kabul edin.")
            
        edge_labels[("Karma/Atalar", "BABA")] = sorun
    else:
        G.add_edge("Karma/Atalar", "BABA", color='green')
        edge_colors.append('green'); edge_styles.append('solid')
        oneriler.append("🌳 **Satürn Desteği:** Baba soyundan gelen dayanıklılık mirasına sahipsiniz.")

    # 2. AY (Anne Bağı ve Ev Konumu) - YENİ EKLENDİ
    anne_sorun = False
    
    # Ay Evi Kontrolleri
    if ay_ev == 12:
        anne_sorun = True
        oneriler.append("🌑 **Ay 12. Ev:** Anne sisteme 'uzak' veya 'ulaşılamaz' hissediliyor olabilir. Anne karnındayken yaşanan bir gizli durum (yas, saklanan gebelik) etkin.")
    elif ay_ev == 8:
        anne_sorun = True
        oneriler.append("🦂 **Ay 8. Ev:** Anne ile ilişki 'krizler' üzerinden yürüyor. Kaybetme korkusu veya derin psikolojik bağlar var.")
    elif ay_ev == 4:
        oneriler.append("🏡 **Ay 4. Ev:** Anne evin temel direği. Ancak köklerin yükünü de o taşıyor. Yuvaya aşırı düşkünlük.")

    # Ay Burcu/Açı Kontrolleri
    if ay_burc in ['Oğlak', 'Akrep'] or ay_aci or anne_sorun:
        G.add_edge("ANNE", "DANIŞAN", color='orange')
        edge_colors.append('orange'); edge_styles.append('dotted')
        edge_labels[("ANNE", "DANIŞAN")] = "ANNE YARASI"
        oneriler.append(f"🤱 **Anne Bağı (Ay {ay_burc}):** 'Senin kaderin sana ait anne, ben sadece senin çocuğunum' cümlesini çalışın.")
    else:
        G.add_edge("ANNE", "DANIŞAN", color='green')
        edge_colors.append('green'); edge_styles.append('solid')

    # 3. GÜNEŞ/SATÜRN (Otorite)
    if saturn_ev in [1, 10]:
        G.add_edge("BABA", "DANIŞAN", color='red')
        edge_colors.append('red'); edge_styles.append('solid')
        edge_labels[("BABA", "DANIŞAN")] = "BASKI"
        oneriler.append("👑 **Otorite Sorunu:** Patronlarınızla yaşadığınız sorunlar babanızla ilgilidir
