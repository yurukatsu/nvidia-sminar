---
title: "Scalable Data Access for Next-Gen Algorithmic Trading"
author: inu
created: 2026-03-18
tags:
  - NVIDIA-GTC-2026
  - algorithmic-trading
  - market-data
  - GPU-computing
  - financial-AI
---

## 会議情報

| 項目 | 内容 |
| --- | --- |
| カンファレンス | NVIDIA GTC 2026 |
| 日時 | 2026年3月19日（木）1:00 - 1:40 AM JST |
| 講演者 | Christina Qi（CEO, Databento） |
| トピック | Data Science - Time Series Forecasting |

## 全体まとめ

Databento CEO の Christina Qi が、アルゴリズミックトレーディングの20年の歴史と AI/ML の台頭、そして市場データの民主化について講演。

アルゴトレーディングは SEC 規制（1996年 Display Rule、2005年 Reg NMS）を契機に電子取引へ移行し、**レイテンシ競争（Race to Zero）** が激化。しかし物理的限界（光速）に到達した現在、競争の軸は**速度から ML/AI による予測力**へシフトしている。実際に ML 駆動型の取引ファーム（Citadel、Two Sigma、DE Shaw、XTX 等）がレイテンシ駆動型ファームを収益で上回っている。

金融における GPU の主な用途は、エキゾチックなモデルではなく**大規模な特徴量エンジニアリング**（10万以上の予測変数、非線形相互作用の探索）であり、クロスバリデーションの並列化が GPU を必要とする主因。LLM はトレーディング戦略には適しておらず、深層学習による非線形回帰と特徴量の組み合わせが現在の最先端である。

## Key Points

### 1. アルゴトレーディングの歴史 — 規制が生んだレイテンシ競争

- **1996年 Display Rule**：マーケットメーカーに ECN（電子取引ネットワーク）での気配表示を義務化 → 取引がフロアから電子市場へ移行
- **2005年 Reg NMS**：最良気配での約定義務（Best Bid/Offer）を導入 → 複数取引所間の価格情報を最速で取得する**レイテンシ競争**が勃発
- マイクロ波ネットワーク、カスタム ASIC、FPGA 等に数億ドルの投資
- 現在は S&P 先物-現物間の反応時間が**光速の理論限界（約5ms）** に到達し、経済的に競争が成立するのは一握りのファームのみ

### 2. 速度から知性へ — ML 駆動型ファームの台頭

- レイテンシ競争はスケールしない（物理的・経済的限界）
- **ML 駆動型トレーディングはスケーラブル**
- S&P トレーディング収益で ML 駆動型4社がレイテンシ駆動型5社を上回る
- DeepSeek は元々クオンツヘッジファンドであり、2021年頃から中国最大級の GPU クラスターを保有していた
- ML 駆動型ファームも高速（FPGA 等を利用）だが、差別化の源泉は ML

### 3. 金融における GPU の真の用途

- **主用途は特徴量エンジニアリング**：基本的なトレーディングモデルでも10万以上の予測変数を使用
- フィンテック（クレジットスコアリング等）の5-20特徴量とは桁違い
- 非線形相互作用（株価変動 × ボラティリティ等）の探索に深層学習が有効
- モデル訓練自体は高速だが、**ハイパーパラメータ最適化とクロスバリデーションの並列化**が GPU を大量に必要とする理由
- GPU の調達は金融業界でも1年以上待ちになることがある

### 4. AI と金融 — 現在の限界と機会

- **LLM はトレーディング戦略には適さない**（講演者が明確に警告）
- IBM Watson の AI ETF は S&P を毎年アンダーパフォーム — 汎用 AI ≠ 金融予測
- 完全自律型 AI ヘッジファンドは未だ存在せず、常に人間がループに存在
- 40年間線形回帰が金融予測の標準 → 非線形回帰（XGBoost、深層学習）への転換が近年のブレークスルー
- 2015年頃から Kaggle 上位は深層学習が独占

### 5. リテール取引の急成長と市場データの民主化

- COVID 後にリテール取引が急増（Robinhood、CalSheet、Polymarket 等）
- CS 学位取得者が過去10年で11倍に増加 → トレーダーの技術力が向上
- AI アシスタントにより API 統合の成功率が上昇
- Databento：35,000以上の顧客に API でリアルタイム・ヒストリカル市場データを提供。年末までに世界第3位の自己ホスト金融データソースに
- **開発者 API 市場は過去1年で10倍に成長**

### 6. NVIDIA テクノロジーの金融業界への波及

- Mellanox（NVIDIA が買収）の VMA、ConnectX がレイテンシ競争の中核技術だった
- 現在は GPU が ML 駆動型トレーディングの基盤
- Databento も NVIDIA テクノロジーを活用し、2年でカテゴリリーダーに
- Jensen Huang が月曜の基調講演で「トレーディング業界は GPU の最大消費者の一つ」と言及

## 講演ノート（トランスクリプト）

> [!abstract]- アルゴトレーディングの歴史 — SEC 規制と電子取引の誕生
>
> 株式は証券取引所だけでなく、**ECN（Electronic Communication Network）** と呼ばれる代替取引場でも取引される。NASDAQ もかつては ECN として出発した。
>
> **1996年 Display Rule**：マーケットメーカーに ECN での気配表示を義務化。取引がフロアから電子市場へ流出。2000年代初頭には電子取引が全体の半分近くに。
>
> **2005年 Reg NMS**：
> - 最小価格刻みの規定
> - Best Bid / Best Offer の概念導入
> - 顧客注文は最良価格で約定される義務
>
> > Every regulation like this, they always have these unintended accidental consequences. This one had a big unintended consequence of introducing a latency race. Thus was the beginning of modern algorithmic high frequency trading.
>
> 複数取引所の気配を最速で把握できるファームが**情報優位**を獲得。取引所も高速ファームのみが利用可能なエキゾチック注文タイプを導入。
>
> 参考資料：
> - Michael Lewis『Flash Boys』（2014年）— HFT を公に知らしめた書籍（ただし定義の誤りや誇張あり）
> - Harvard Business School ケーススタディ（Christina Qi の前職 Domeyard LP について）— より正確な業界史

> [!abstract]- レイテンシ競争（Race to Zero）— 光速への到達
>
> Reg NMS 後、数十億ドルが投じられ、約10年でファームは光速の物理限界に接近。2008年金融危機は HFT ファームにとって黄金期であり、イノベーションを加速させた。
>
> - ロンドン-フランクフルト間のマイクロ波ネットワーク（最短経路の競争）
> - NJ-シカゴ間（S&P 現物-先物）の反応時間：2014年までに約5ms（理論的な光速限界に近い）
> - 単一データセンター内ではカスタム ASIC 製造で最後のナノ秒を追求
> - Mellanox の VMA、ConnectX、高速スイッチが競争の中核技術
>
> > Today the fastest trading firms can react to the markets within single digit nanoseconds. The race to zero is pretty much over in the sense that it's economically unfeasible for more than a handful of firms to compete.
>
> カスタム ASIC、プライベートマイクロ波ネットワークの構築には数億ドルが必要。スタートアップが参入する意味はほぼない。

> [!abstract]- 予測の時代 — 線形回帰から深層学習へ
>
> > If everyone's already reacting at the speed of light, how can you have an edge? You have to forecast things before they happen.
>
> - **40年間、線形回帰が金融予測の標準**（CAPM、Fama-French 等）
> - 世紀の変わり目に非線形回帰のブレークスルー（ノイズ・限定データへのロバスト性）
> - テック企業によるオープンソース運動：XGBoost、PyTorch、TensorFlow
> - 2015年頃、Kaggle リーダーボードは深層学習が独占
> - **TensorFlow（ソフトウェア）× NVIDIA Tesla GPU（ハードウェア）が金融予測の変曲点**を生む

> [!abstract]- Domeyard LP — Christina Qi の HFT ファーム経験
>
> MIT 卒業直後に HFT ファーム Domeyard LP を設立。ケンブリッジのアパートにサーバーラックを持ち込み、Home Depot と IKEA のパーツで冷却システムを自作。
>
> - Flash Boys 出版（2014年）の2年前、2012年に創業
> - 数年の試行錯誤の後、低レイテンシハードウェア + 深層学習モデルの組み合わせで成功
> - **CME で日次70億ドル以上の取引**、平均日次出来高の約7%を占める最大級のマーケットメーカーに
>
> > We went through essentially every phase of that modern evolution firsthand.

> [!abstract]- 金融における GPU の実際の用途
>
> > Most firms that use GPUs in this industry are not doing anything super exotic. The cutting edge is feature engineering.
>
> - フィンテック（クレジットスコアリング）：5-20特徴量
> - トレーディング：**基本モデルでも10万以上の予測変数**
> - 中央の画像は典型的な予測変数セットの相関行列（各ピクセルが1つの予測変数）
> - 非線形相互作用の探索（株価変動 × ボラティリティ等）に深層学習が威力を発揮
> - 最終モデルの訓練は高速だが、**最適化・クロスバリデーションの並列化**が GPU の大量消費要因
>
> GPU 調達は金融業界でも困難で、1年以上待ちになることも。

> [!abstract]- 速度 vs 知性 — 誰が勝ったか
>
> S&P トレーディング収益の比較：
> - **レイテンシ駆動型**：5社（米欧で最速と見なされるファーム）
> - **ML 駆動型**：4社（XTX が最新参入）
>
> > The four firms in ML-driven trading are making the most revenue right now.
>
> - ML はスケーラブル、レイテンシ競争はスケールしない
> - ML 駆動型ファームも高速だが、差別化の源泉は ML
> - **DeepSeek**：元クオンツヘッジファンド。2021年頃から中国最大級の GPU クラスターを保有していたことは業界内では既知

> [!abstract]- リテール取引の急成長と AI の影響
>
> - COVID 後にリテール取引が急増。あらゆる属性向けの取引アプリが登場
> - CS 学位取得者が過去10年で11倍 → トレーダーの技術力が向上
> - AI アシスタントにより API 統合が容易に → 開発者 API 市場が**過去1年で10倍成長**
>
> > You don't need to be a true expert at the cutting edge now. You just need to know the fundamentals, and then you just need to be able to use AI to go from there.

> [!abstract]- AI と金融 — 現在の限界
>
> > Language models are not algorithmic trading models. Please don't plug in quantitative strategies into language model stuff and trust your language model to do trading strategies. That is not a good idea today.
>
> - IBM Watson の AI ETF は S&P を毎年一貫してアンダーパフォーム
> - 完全自律型 AI ヘッジファンドは未だ存在しない — 常に人間がループに存在
> - AI は金融で長年語られてきたが、実際の成功は最近まで限定的
> - 成功の鍵は LLM ではなく、**非線形回帰 + 大規模特徴量エンジニアリング + GPU 並列化**

> [!abstract]- Databento と NVIDIA の活用
>
> - Databento：35,000以上の顧客に API で市場データ提供。リアルタイム + ヒストリカル
> - 年末までに世界第3位の自己ホスト金融データソースに（ローンチから約2年）
> - NVIDIA テクノロジーを活用し2年でカテゴリリーダーに成長
> - NVIDIA の Web サイトで最初の金融スタートアップ成功事例として紹介（NASDAQ に次いで）
> - コロケーション接続、クラウドソリューション、クロスコネクトも提供
>
> **Q&A**（Morgan Stanley Vadim からの質問）：
> - Q: ヒストリカル分析寄りかリアルタイム取引用途か？
> - A: 両方提供。リアルタイムデータがより有用。ヒストリカルデータだけでは「バックミラーで運転しているようなもの」。HFT 向けコロケーション接続も提供。
> - Q: NASDAQ のデータか？Bloomberg との競合は？
> - A: 米国には20以上の証券取引所がある。Bloomberg はデータアグリゲーター/チャートツールであり、取引所ではない。Databento は取引所から直接データを取得し API で提供。

## 当チームへの示唆

- **ML 駆動型トレーディングの優位性**：レイテンシから ML/AI へのパラダイムシフトは、セールス&トレーディング部署の戦略方向性を考える上で重要な背景情報。速度ではなく予測力とシグナル生成が競争優位の源泉になりつつある
- **特徴量エンジニアリングの規模**：10万以上の予測変数を扱うトレーディングモデルの実態は、当チームのモデル設計における特徴量の網羅性と GPU リソース計画の参考になる
- **LLM ≠ トレーディング戦略**：講演者が明確に警告。LLM はフロントオフィスツールやテキストデータ分析には有用だが、定量的取引戦略の直接的な代替にはならない。当チームでも生成 AI の適用範囲を適切に見極める必要がある
- **Databento API の活用可能性**：市場データの取得・分析が API 経由で容易に。リサーチの高速化や新しいデータソースとしての検討に値する
- **非線形モデルの有効性**：40年間の線形回帰 → 非線形モデル（深層学習、XGBoost）への転換が実績として示されており、市場データ分析のモデリングアプローチの見直しの根拠となる
