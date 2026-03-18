---
title: "Optimizing $1 Trillion in Payments: From Contextual Bandits to Foundational Models"
author: inu
created: 2026-03-18
tags:
  - NVIDIA-GTC-2026
  - reinforcement-learning
  - foundation-model
  - payments-optimization
  - contextual-bandits
---

## 会議情報

| 項目 | 内容 |
| --- | --- |
| カンファレンス | NVIDIA GTC 2026 |
| 日時 | 2026年3月18日（水）20:00 - 21:00 JST |
| 講演者 | Dhruv Ghulati（Principal AI Product Manager, Adyen） |
| トピック | Agentic AI / Generative AI - Code / Software Generation |

## 全体まとめ

世界最大級の決済プロバイダー Adyen（年間売上 23億ユーロ、日次1.2億トランザクション）が、決済最適化における ML アプローチの進化を紹介したセッション。

決済は「承認率最大化」「コスト最小化」「不正防止」の3つの相反する目標を持つ多目的最適化問題であり、Adyen はこれを **Contextual Bandit** として定式化。ルールベース → 教師あり報酬モデリング → Contextual Bandit → Deep Learning（Self-Attention → Causal Attention → Deep & Cross Network）と段階的にアプローチを進化させた。

さらに、手動特徴量エンジニアリングからの脱却を目指し **Foundation Model**（PaymentBERT → テキストベースシーケンスモデル → 階層的ファウンデーションモデル）の構築に着手。約2000億件の決済データ（約50兆トークン、Llama 4 の訓練データの2倍以上）で事前学習を行い、全社横断の共有表現基盤として活用している。

## Key Points

### 1. Adyen Uplift — 決済最適化プロダクトスイート

| モジュール | 機能 | 成果 |
| --- | --- | --- |
| **Personalize** | チェックアウト画面の決済手段ランキング最適化 | コンバージョン率最大6%改善 |
| **Tokenize** | ネットワークトークンへの置換、カード情報自動更新 | — |
| **Protect** | ML ベースの不正検知 | コンバージョン10%増、不正率41%減 |
| **Authenticate** | リスクベース認証（SMS、Face ID、銀行アプリ等） | — |
| **Optimize** | ML によるルーティング・メッセージング最適化 | 米国でコスト最大20%削減、承認率89bp改善 |

全体で **1.2% のコンバージョン率向上**。2025年に673件の実験を実施（うち287件が最適化モデル関連）。

### 2. 決済の Contextual Bandit 定式化

- **State**：マーチャント設定、BIN（8桁）、発行銀行、金額、リトライ回数、行動シグナル等
- **Action**：ルーティングパス × 認証戦略 × ISO メッセージ設定 → **20,000以上の組み合わせ**
- **Reward**：発行銀行の認証判定（Adyen からは観測不能な内部リスクエンジン）
- **課題**：探索に直接的な経済コスト（リアルタイムのコンバージョンに影響）、発行銀行の行動ドリフト、規制制約

### 3. Deep Learning モデルの進化

| ステージ | アプローチ | 解決した課題 |
| --- | --- | --- |
| ルールベース | 静的ルール | — |
| 教師あり学習 | Boosting（GBT） | ドリフト非対応、最適ポリシーではなく過去の報酬を学習 |
| Contextual Bandit | 制御された探索 | 報酬推定のスケーリング問題 |
| Self-Attention | カテゴリ特徴量の埋め込み + Multi-head Attention | 本番で不安定 |
| **Late Attention** | 中間交差表現を先に生成してから Attention | 時間的リーク（将来情報の混入） |
| **Causal Attention** | 意思決定時に利用可能な情報のみに Attend 制限 | 特徴量衛生・オフポリシー評価の妥当性確保 |
| **Deep & Cross Network** | 明示的高次特徴交差 → 非線形深層 | 安定性・レイテンシ効率 |
| **Structured Sparsity** | 主要トークン（issuer/scheme）に固定した制約付き交差 | 組合せランキングの分散低減 |

### 4. Foundation Model の構築

**進化の軌跡**：

| 年 | アプローチ | 特徴 |
| --- | --- | --- |
| 2024 | **PaymentBERT** | トランザクション＝文、フィールド＝トークン。MLM で事前学習。単一トランザクションのみ |
| 2025 | **テキストベースシーケンスモデル** | 決済シーケンス全体をテキストに直列化。長距離行動モデリング可能だが文脈窓の二次スケーリング問題 |
| 2025 | **Multi-View Embeddings** | Shopper/Card/Merchant/Market の複数視点表現。各チームが必要なビューを選択して専用ヘッドを接続 |
| 2026 | **階層的ファウンデーションモデル** | Transaction → Entity → Merchant → Market の多階層エンコーダ。要約によるコンテキスト窓効率化 |

**事前学習規模**：約2000億件の決済、約50兆トークン（Llama 4 は22兆トークン）。MLM + Next Event Prediction + Contrastive Learning 等の自己教師あり学習。

### 5. デプロイとインフラ

- **SLA**：ピーク時3,000 TPS、P50 レイテンシ 20ms、30ms 以下をほぼ100%
- **アーキテクチャ**：エンティティ埋め込みをオフラインで事前計算・キャッシュ + 軽量オンラインアダプタで推論
- **ハードウェア**：NVIDIA A100 GPU（大容量 VRAM による将来性）
- **インフラ技術**：RDMA（GPU 間通信）、Ray（シャーディング・スケーリング）、Kubernetes + NVIDIA GPU Operator、MIG（1基の A100 を最大7インスタンスに分割し利用率最大化）
- **障害対応**：自動検知・フェンシング、トポロジー認識オーケストレータ

### 6. ケーススタディ — Shopper Linking

- タスク：2つのトランザクションが同一ショッパーか判定（15億人規模）
- 埋め込みモデルが精度-再現率曲線全域で最良
- 再現率80%時に**精度20%改善**、合成ショッパー分離で **ARI 170%向上**
- 表層識別子ではなく潜在的な行動構造を捉えることで、疎なマーチャント・発行銀行間のインタラクションでも分散を低減

### 7. 将来ビジョン — 統合オーケストレータ

- ルーティング・認証・不正検知・コスト最適化を**単一のオーケストレータ層**で統合
- RL エージェントが Foundation Model 埋め込みを活用し、フルファネルの純収益（コスト + コンバージョン + 下流リスク）を最適化
- ユーザーがコスト・コンバージョン・不正の優先度を設定 → システムが最適な決済設定を自動推奨・実装

## 講演ノート（トランスクリプト）

> [!abstract]- Adyen と決済の仕組み
>
> Adyen は世界最大級の決済プロバイダー。Adidas, Uber, McDonald's, Spotify, Microsoft 等が利用。2023年の純収益は約23億ユーロ（前年比18%増）。アムステルダム本社、28拠点、約4,000名。
>
> > If a shopper shows up at a merchant for the first time, there's an 84% chance that Adyen has seen that shopper before.
>
> 決済フロー：API/チェックアウト/POS からリクエスト受信 → トークン化 → 不正リスクチェック → 認証 → ルーティング最適化 → ISO メッセージ送信 → 発行銀行の認証取得 → 資金移動。全てリアルタイム。
>
> マーチャントの3つの目標：
> 1. 成功する決済の最大化（コンバージョン）
> 2. トランザクション手数料の最小化（コスト）
> 3. 不正・紛争の防止（リスク）

> [!abstract]- Adyen Uplift プロダクトスイート
>
> 2025年にローンチした決済最適化スイート。複数モジュールを統合：
>
> - **Personalize**：チェックアウト画面の決済手段ランキング最適化。コスト重視なら地域決済手段を上位に、コンバージョン重視なら最も成功率の高い手段を表示
> - **Tokenize**：ネットワークトークンへの置換。マーチャント単位で生成されるため漏洩時も安全。リアルタイムカード情報更新
> - **Protect**：ML ベース不正検知
> - **Authenticate**：リスクベース認証。高リスクはチャレンジ（ブロックではなく）、低リスクはフリクションレス通過
> - **Optimize**：ML によるスキームパフォーマンス・発行銀行行動・コスト構造のリアルタイム分析でルーティング最適化
>
> > Our overall product suite has led to about a 1.2% extra uplift on conversion rates. On fraud detection, we've led to an overall about 10% increase in conversion and a 41% drop in fraud rates.

> [!abstract]- Contextual Bandit としての決済最適化
>
> > Every transaction arises with a really rich high-dimensional state. We then choose a structured action consisting of a routing path, an authentication strategy, and a specific ISO message configuration. The reward is the issuer's authorization decision, and it comes from that issuer's internal risk engine that we don't know about.
>
> **Inter-scheme routing**：デュアルブランドカード（例：MasterCard + Star）で最適ネットワークを選択
> **Intra-acquirer routing**：同一ネットワーク内で異なる商業設定（例：MCC 変更）で発行銀行のリスク認識を調整
> **Smart payment messaging**：ISO メッセージのフィールド・フラグを調整してルーティングを変えずに承認率改善
>
> アクション空間：ルーティング最大10パス × メッセージング30+フラグ → **20,000以上の組み合わせ**。構造化された組合せ的 Contextual Bandit。
>
> > Exploration has a direct economic cost. Whenever we change ISO messages or routes in an online setting, we are actually affecting the conversion rates of that customer in real time.

> [!abstract]- ML モデルの進化：ルールから Deep Learning へ
>
> 1. **ルールベース**：集約データに基づく静的ルール。ドリフト非対応、手動チューニング
> 2. **教師あり報酬モデリング（Boosting）**：過去のアクションから承認確率を推定。最適ポリシーではなく既存ポリシーの報酬を学習してしまう
> 3. **Contextual Bandit**：制御された探索を導入。しかし巨大アクション空間での報酬推定がスケールしない
> 4. **Self-Attention Deep Learning**：カテゴリ特徴量の埋め込み + Multi-head Attention。本番で不安定
> 5. **Late Attention**：中間交差表現を先に生成してから Attention。安定化したが時間的リーク問題
> 6. **Causal Attention**：意思決定時に利用可能な情報のみに制限。フラグ特徴量を因果的に最重要に固定
>
> > If post-decision signals leak into training, the model can exploit correlations that disappear once you intervene. Offline it looks great, but online it collapses.
>
> 7. **Deep & Cross Network**：明示的高次特徴交差。スパースカテゴリドメインで効果的、Attention より安定・低レイテンシ
> 8. **Structured Sparsity**：主要トークン（issuer/scheme）に固定した制約付き交差。組合せランキングの分散低減
>
> > In 2025 alone, we ran about 673 experiments across all ML models. With 287 focused on the main optimization model. Even fractional improvements, like a 0.1% uplift in authorization, can translate to massive incremental GMV. Precision dominates novelty in high-scale machine learning.

> [!abstract]- Foundation Model の構築 — PaymentBERT からの進化
>
> **動機**：従来はタスク固有モデルが手作り集約特徴量で独立にトランザクションを処理。決済は本質的にシーケンシャル・エンティティベース・マルチタスク。
>
> **PaymentBERT（2024）**：トランザクションを文、フィールド（BIN, merchant ID, amount 等）をトークンとして扱う BERT。CLS トークン + Transformer エンコーダ + MLM で事前学習。
>
> **テキストベースシーケンスモデル（2025）**：決済シーケンス全体をテキストに直列化。
> - Pros：情報ボトルネックなし、end-to-end 学習、単一語彙
> - Cons：文脈窓の二次スケーリング、ブラックボックス化、データ大量消費
>
> **Multi-View Embeddings（2025）**：Shopper/Card/Merchant/Market の複数視点。
>
> > If you were only looking at shopper behavior, buying a watch would be anomalous and fraudulent. But if you combine it with the merchant's view, you can know that buying a watch for that specific merchant was not an anomaly at all.
>
> **階層的ファウンデーションモデル（2026）**：
> - Transaction → Entity → Merchant → Market の多階層エンコーダ
> - Prior Encoder がベイジアン事前分布として機能
> - 階層的フュージョンで要約埋め込みを統合
> - Pros：解釈可能性、コンテキスト窓効率化、ドメイン知識の注入
> - Cons：要約による情報ボトルネック、共同目的関数のモデル崩壊リスク

> [!abstract]- 事前学習と規模
>
> エンコーダのみアーキテクチャ、自己教師あり学習（ラベル不要）。
>
> > Our embeddings are trained on around 200 billion payments, which amounts to about 50 trillion tokens. Llama 4 was only trained on 22 trillion tokens.
>
> 学習タスク：MLM（構造トークンのマスク予測）、Next Event Prediction、Contrastive Learning（同一/異なるショッパーの識別）、Cohort Discrimination、Temporal Consistency。
>
> 評価：クラスタリング効果、近傍一貫性、線形分離可能性。下流タスクでは埋め込みを凍結し MLP/ロジスティック回帰で AUROC/Log Loss を評価。

> [!abstract]- デプロイとインフラ（NVIDIA 活用）
>
> > Payments require millisecond level decisioning. Our SLAs require us to hit below 30 milliseconds almost 100% of the time. Full sequence transformers can't run per request. We pre-compute entity embeddings offline and cache them. Lightweight online adapters combine new transaction context.
>
> **ハードウェア**：NVIDIA A100 GPU。大容量 VRAM が必須。イテレーション時間を数日→数時間に短縮。PyTorch、Flash Attention、Gradient Checkpointing との統合。
>
> **通信**：RDMA で GPU 間最適通信。ネットワークボトルネック解消。
>
> **耐障害性**：自動検知・フェンシング。将来的に自動リカバリ。
>
> **スケーリング**：Ray でシャーディング・スケーリング管理。トポロジー認識オーケストレータ。
>
> **リソース共有**：Kubernetes + NVIDIA GPU Operator + **MIG**（A100 を最大7インスタンスに分割。小規模ジョブに適切なサイズのリソースを提供し利用率最大化）。

> [!abstract]- ケーススタディ：Shopper Linking と埋め込み評価
>
> 地球上の約15億人の個人に対し、Adyen プラットフォーム上の行動パターンからアイデンティティを確立するタスク。
>
> 3つのアプローチを比較：
> 1. Greedy identifier-based matcher
> 2. One-hot + hashing model（明示的特徴量）
> 3. **Payment embeddings**（Foundation Model）
>
> > The embeddings dominated the precision-recall curve across the entire range. At 80% recall, we observed roughly a 20% precision improvement. On synthetic shopper disentanglement, we found actually 170% increase in ARI.
>
> 埋め込みが表層識別子ではなく潜在的行動構造を捉えたことで、疎なインタラクションでも分散が低減。上流の表現改善が下流のエンティティ解決を堅牢化。

> [!abstract]- 将来ビジョン：統合オーケストレータと RL エージェント
>
> > Today, routing, authentication, and fraud models optimize partially different objectives. When optimized independently, they produce local optima rather than globally efficient outcomes.
>
> **統合システムの定式化**：
> - State：Foundation Model の学習済み埋め込み
> - Action：ルーティング + 認証戦略 + 不正介入
> - Reward：フルファネルの純収益（コスト + コンバージョン + 下流リスク）
>
> **オーケストレータ層**：ルーティング・認証・不正・コストを横断的に統括。各モデルがコンバージョン・コスト・リスクの期待値を推定し、ユーザー設定の制約に基づき動的にパラメータ調整。
>
> > You can imagine a system where a user can just set design preferences for cost, conversion, and fraud. And then we could suggest new implementations and changes, including new payment methods, and even implement them automatically.

## 当チームへの示唆

- **Contextual Bandit の適用パターン**：多数のアクション選択肢と経済的コストのある探索を伴う意思決定問題の定式化として参考になる。セールス&トレーディングにおける注文ルーティングや執行戦略の最適化に類似の構造がある
- **Causal Attention の設計**：時間的リーク（将来情報の混入）を構造的に防ぐアーキテクチャは、金融時系列モデルの設計で重要。特にバックテストとライブ性能の乖離を防ぐ手法として有用
- **Foundation Model のアプローチ**：タブラー/トランザクションデータに対する BERT 風事前学習（フィールド＝トークン）と Multi-View Embeddings は、市場データや取引データの表現学習に応用可能
- **Multi-View Embeddings**：エンティティ（トレーダー、顧客、商品等）ごとに異なる視点の埋め込みを学習し、タスクに応じて組み合わせるアーキテクチャは、当チームの分析基盤にも展開できる設計パターン
- **小さな改善の複利効果**：0.1% の精度改善が兆円規模のトランザクションでは巨大なインパクトになるという実例。当チームのモデル改善の ROI 評価にも同様の視点が重要
- **MIG による GPU リソース共有**：A100 の MIG 分割による利用率最大化は、GPU リソースが限られる環境でのチーム間共有戦略として検討に値する
