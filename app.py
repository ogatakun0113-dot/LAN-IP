import streamlit as st
import ipaddress

# --- ページ設定 ---
st.set_page_config(page_title="IPv4サブネット計算アシスト", layout="centered")

# --- 見た目の設定（CSS） ---
st.markdown("""
    <style>
    /* クレジット表示用のCSS */
    .credit {
        text-align: right;
        font-size: 14px;
        color: #666;
        margin-bottom: -20px;
    }
    /* 入力欄のラベルスタイル（ネットワーク系なのでオレンジ〜紫系） */
    .stTextInput label, .stSelectbox label {
        font-size: 18px !important;
        color: #FF8C00 !important; /* ダークオレンジ */
        font-weight: 800 !important;
    }
    /* 計算結果ボックス */
    .result-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FF8C00;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 右上にクレジットを表示
st.markdown('<p class="credit">開発/制作：緒方</p>', unsafe_allow_html=True)

st.title('🌐 IPv4 サブネット計算アシスト')
st.caption("※ルーター設定やVPN（Instant Guard等）のネットワーク設計に")
st.markdown("---")

# --- 入力セクション ---
col1, col2 = st.columns([2, 1])

with col1:
    ip_input = st.text_input("IPアドレスを入力", value="192.168.1.1")
with col2:
    # 一般的に使われるサブネットマスクのリスト
    cidr_list = [i for i in range(32, 7, -1)]
    prefix = st.selectbox("CIDR (prefix)", cidr_list, index=cidr_list.index(24))

try:
    # 入力されたIPとプレフィックスからネットワークを生成
    # strict=Falseにすることで、ホストアドレスからでもネットワーク計算が可能
    net = ipaddress.IPv4Interface(f"{ip_input}/{prefix}").network

    # --- 計算結果の取得 ---
    net_addr = net.network_address
    broadcast = net.broadcast_address
    netmask = net.netmask
    wildcard = net.hostmask
    num_hosts = net.num_addresses
    
    # 利用可能ホスト（ネットワークアドレスとブロードキャストを除く）
    if num_hosts > 2:
        first_host = net.network_address + 1
        last_host = net.broadcast_address - 1
        usable_hosts = num_hosts - 2
    else:
        # /31 や /32 の特殊なケース
        first_host = "N/A"
        last_host = "N/A"
        usable_hosts = num_hosts

    # --- 表示セクション ---
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.subheader("📊 計算結果")
    
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**ネットワークアドレス:** `{net_addr}`")
        st.write(f"**サブネットマスク:** `{netmask}`")
        st.write(f"**ブロードキャスト:** `{broadcast}`")
    with c2:
        st.write(f"**最初のホスト:** `{first_host}`")
        st.write(f"**最後のホスト:** `{last_host}`")
        st.write(f"**利用可能ホスト数:** `{usable_hosts}`")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # 補足情報
    with st.expander("詳細なビット情報"):
        st.write(f"**ワイルドカードマスク:** `{wildcard}`")
        st.write(f"**バイナリ形式 (Netmask):** `{bin(int(netmask))}`")

except ValueError:
    st.error("正しい形式でIPアドレスを入力してください（例: 192.168.1.1）")

st.markdown("---")
st.caption("💡 ヒント: ASUSルーターのLAN設定では通常 /24 (255.255.255.0) が標準的です。")


# --- 画面下部中央に「戻る」ボタンを配置 ---
st.markdown("---")  # 区切り線
col1, col2, col3 = st.columns([1, 1, 1])

with col2:  # 中央の列を使用
    # 水色のアイコン（🏠）と「戻る」を表示するボタン
    if st.link_button("🏠\n\n戻る", "https://7fjndw39dicdzckugyepb2.streamlit.app/", use_container_width=True):
        pass

# ボタンの色（水色）を調整するカスタム設定
st.markdown("""
    <style>
    div.stLinkButton > a {
        background-color: #00BFFF !important; /* 水色（DeepSkyBlue） */
        color: white !important;
        border-radius: 10px;
        text-align: center;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

