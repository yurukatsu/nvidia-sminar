---
title: "Beyond the Black Box: Interpretability of LLMs in Finance"
author: inu
created: 2026-03-18
tags:
  - NVIDIA-GTC-2026
  - mechanistic-interpretability
  - LLM
  - trading
  - risk-management
---

## 会議情報

| 項目 | 内容 |
| --- | --- |
| カンファレンス | NVIDIA GTC 2026 |
| 日時 | 2026年3月17日（火）22:00 - 22:50 JST |
| 講演者 | Hariom Tatsat（VP, Risk AI, Barclays）、Ariye Shater（MD, Head of Risk AI, Barclays） |
| トピック | Trustworthy AI / Cybersecurity - Security for AI |
| 関連論文 | セッション内で QR コードにて共有（Barclays Risk AI チームによる MechInterp 論文） |

## 全体まとめ

Barclays の Risk AI チームが、LLM の内部構造を解析する**機械的解釈可能性（Mechanistic Interpretability, MechInterp）**の金融応用について発表したセッション。従来の解釈手法（SHAP、LIME 等）がモデルの入出力を外側から観察するのに対し、MechInterp はニューロンや層の内部に踏み込み、モデルの推論メカニズムをリバースエンジニアリングする。「AI の脳神経科学」「AI の MRI」とも呼ばれるアプローチである。

主要ツールである **Sparse Autoencoder（SAE）** を用いて LLM の残差ストリームを解析し、金融に特化した3つのユースケース（クレジットセンチメント分析、トレーディングシグナル抽出、ハルシネーション抑制）を実証。さらに今後の研究として、古典的ファクターモデルへの LLM 特徴量の統合やエージェント AI のリアルタイム監視への応用も紹介された。

## Key Points

### 1. なぜ金融で解釈可能性が必要か

- **85%** の AI パイロットが POC 段階で停滞 → 70% が説明可能性の欠如に起因
- **0%** — エンタープライズ環境でモデル内部を観察するツールがほぼ存在しない（プロンプト・CoT・ガードレールは全て外側からのアプローチ）
- **$20 兆** — 2008年金融危機の損失額。金融モデルを十分に理解しなかった結果であり、より複雑な AI モデルでも同様のリスクがある

### 2. 機械的解釈可能性（MechInterp）のツール群

| ツール | 概要 |
| --- | --- |
| **Sparse Autoencoder（SAE）** | 残差ストリームにタップし、ポリセマンティシティ（1つのニューロンが複数概念を表現）を解きほぐす。特徴量を人間が読めるラベルに変換可能 |
| **LogitLens** | 各層での次トークン予測を可視化。層ごとの寄与度を把握するが、層レベルの粒度に留まる |
| **Linear Probe** | LLM 内部層を予測モデルの変数として活用。価格の上下やトキシシティの予測に使用 |
| **Circuits** | 複数層にまたがる特徴量の結合・情報フローを追跡（LogitLens + SAE の組み合わせ）。Anthropic の "Biology of LLMs" 論文で紹介された Transcoder も関連 |

### 3. ユースケース① — クレジットセンチメント分析（Feature Steering）

- SAE でクレジットリスク関連の特徴量を特定し、その活性化を増幅（**ステアリング**）
- プロンプト変更やファインチューニングなしで、汎用センチメントからクレジット特化のセンチメントに調整可能
- 事前ラベル付きデータセットで検証した結果、ステアリング後にセンチメント分類精度が向上

### 4. ユースケース② — Warren Buffett AI（トレーディングシグナル抽出）

- 過去10年・10,000件以上の金融ニュースヘッドラインを SAE に通し、活性化の高い約300特徴量を選定
- それらの特徴量活性化値を入力として、S&P500・Apple の価格変動（上/下）を予測する Random Forest を訓練
- 最も重要な特徴量は **Named Entity Recognition（場所名）**、次いで金融用語、ティッカーシンボル等 → 既知の金融 NLP 知見と整合
- **核心的な発想**：LLM の脳には株式市場の歴史・価格アノマリー・マクロレジーム等が既に内包されており、SAE でその「針」を見つけ出す

### 5. ユースケース③ — Hallucination Police（ハルシネーション抑制）

- 金融関連の特徴量を事前選定し、質問応答時にそれらの活性化をモニタリング
- 活性化が閾値未満の場合、プロンプト拡張（SEC ファイリング等の追加コンテキスト）を自動注入
- 結果：回答が詳細化し、引用付きの根拠ある出力に改善（例：8-K の提出期限に関する質問で、例外項目や SEC 規則の引用まで出力）

### 6. 今後の研究方向

- **古典的ファクターの拡張**：S&P500リターン、ボラティリティ等の伝統的ファクターに、LLM 内部の特徴量（インサイダー買い、アーニングミス、M&A 関連等）を追加してモデルを強化
- **エージェント監視（Agentic Monitoring）**：エージェント実行中の推論プロセスを SAE でリアルタイム監視し、ツール呼び出しの誤りを検出・停止・修正。コスト削減にも寄与

### 7. 技術スタックと制約

- **使用環境**：PyTorch + NVIDIA CUDA、NVIDIA Launchpad（H100 GPU × 8）
- **制約事項**：
  - オープンウェイトモデルが必須（クローズドモデルの内部は観察不可）
  - 現時点では単一層の解析に限定（Circuits による多層解析は計算コストが高い）
  - 解釈可能性の定量的メトリクスが未成熟

## 講演ノート（トランスクリプト）

> [!abstract]- イントロダクション — なぜ解釈可能性が必要か
>
> **Ariye Shater**: We are a team of AI quants that focus on AI applications across all of Barclays, including risk finance, and trading. We're going to talk about a very important topic that we've written a paper about that really focuses on understanding how LLMs work.
>
> **Hariom Tatsat**: For this paper, we used a lot of resources from the researchers, from OpenAI, DeepMind, Anthropic, their papers, their code. And we gave a tweak for those research and gave a financial angle to that.
>
> スライドに3つの数字が提示された：
>
> - **85%** — AI パイロットが本番に到達しない割合。70% のリーダーが説明可能性の欠如に起因すると回答
> - **0%** — エンタープライズでモデル内部を観察する Gen AI ツールの数。プロンプト、CoT、ガードレールは全て外側からのアプローチ
> - **$20 trillion** — 2008年金融危機の損失額。金融モデルを十分に理解しなかった結果
>
> > We didn't understand the financial models really well in 2008. Now we have all these AI models, which are even more complex. These are even more ingrained in the workflows of the organization. And if we don't understand it well, we might be at loss again.
>
> > If we are not satisfied with the answer we get from ChatGPT or AI models, we just try to run it again and again till we reach a really good state. It's good. Everybody does that. But it doesn't work in the enterprise setup, especially in the high-stake domains like finance. You need to have more deterministic output. You need to understand the models really well.

> [!abstract]- 解釈可能性の種類と機械的解釈可能性（MechInterp）
>
> 従来の解釈可能性手法：
>
> 1. **Feature Attribution** — SHAP, LIME, Integrated Gradients 等。入力の何%がこの不正に寄与しているか
> 2. **Model Simplification** — より単純なモデルを使い変数を可視化。金融で単純モデルが好まれる理由の一つ
> 3. **Behavioral Interpretability** — 感度テスト。入力にショックを与え出力への影響を観察
> 4. **Visual Explanation** — 入力マップの可視化
> 5. **Mechanistic Interpretability** — 上記全てと異なり、モデル内部に踏み込む
>
> > We call it neuroscience of generative AI. Some people also call it MRI for AI. Unlike other types of interpretability techniques, we go deeper into the neurons and the layers, and we reverse engineer that.
>
> 糖尿病の例え：従来手法は「何を食べているか」のパターン分析。MechInterp は「脳の中の砂糖渇望を担当するニューロンを見つけ、その影響を減らす」アプローチ。
>
> **Ariye Shater（モデルリスク管理の文脈）**:
>
> > Post financial crisis, the trust in models went almost to zero. We couldn't trust our models to measure our risk, to produce valuations. So we introduced a process where we have independent functions inside banks that review and verify the models. The same could be said by regulators. Lehman Brothers — I used to work there — it caused a systemic risk. Hence, AI has a chance of causing a systemic risk. Hence, we need to understand it, how it works.

> [!abstract]- ツール：Sparse Autoencoder（SAE）— LLM の顕微鏡
>
> **Ariye Shater**: I think of it as a way to zoom in and understand how models interpret the input and output data.
>
> SAE が必要な理由は**ポリセマンティシティ**。モデルはパラメータを異なる概念で再利用する（例：天体物理学とマイケル・ジョーダンが同じニューロンで表現される）。特徴量の分離が困難。
>
> > We create this microscope to zoom in into residual stream of a network. By making it sparse, you're effectively disentangling the features inside the model.
>
> 例：「What is the capital of France?」→ SAE を残差ストリームに適用すると、French culture, French flag, Eiffel Tower, wine, baguette 等の特徴量が形成される。モデルが正しい特徴量に関連付けて Paris と回答していることが確認できる。
>
> SAE は残差ストリームへの「タップ」。Layer 2 の残差ストリームを SAE に通すと、犬と猫の分離、車と木の認識等が観察できる。処理後のデータは Layer 3 に渡される。複数層にタップすることで、ネットワーク全体の特徴量形成を追跡可能。

> [!abstract]- ツール：特徴量ラベリング、ステアリング、クラスタリング
>
> **特徴量ラベリング**：SAE の出力は数値。多数の文・キーワード・記事を通し、最も活性化するコンテキストでラベルを付与。例：London というキーワードで頻繁に活性化する特徴量 → "references to London" とラベリング。
>
> **ステアリング（Ariye Shater）**：
>
> > You actually ask a model to describe the feature. You take a particular feature, a vector of numbers, and you scale it up and down. Once you increase the scale, you ask the neural network "what is the meaning of word X?" and the model describes itself what the features are. It's a fascinating concept of letting model to self-intervene itself.
>
> 特定の特徴量のスケールを上げてモデルに「この特徴量は何か」と問うと、モデル自身がその特徴量を説明する。
>
> **特徴量クラスタリング**：ラベリング後、類似特徴量をベクトル類似度でクラスタリング。金融特化クラスタとして以下が形成された：
> - Climate change / Renewable energy
> - Market risk / Price performance（投資クラスタ）
> - Payments and taxes
> - Banking, finance, transaction, wealth management

> [!abstract]- ツール：LogitLens, Linear Probe, Circuits
>
> **LogitLens（Hariom）**: 各層で次トークン予測を確認。浅い層では非直感的な結果、深い層ほど直感的に。どの層が最大の価値を付加しているか把握できるが、層レベルの粒度に留まる。
>
> **Linear Probe**: LLM 内部層のニューロンを変数として予測モデルを構築。ニュース記事 → 価格上下の予測等。内部表現はコンテキストがリッチで、外部特徴量より強力。トキシシティや有害性の予測にも使用。
>
> **Circuits**: LogitLens + SAE の組み合わせ。複数層にまたがる特徴量の結合・情報フローを追跡。
>
> > 例：「The capital of state containing Dallas is」→ Layer 1 で Capital, State, Dallas が活性化 → 次のレベルで Capital + Texas に結合 → 最終的に Austin を出力
>
> Anthropic の "Biology of Large Language Models" で紹介された **Transcoder**（LogitLens + SAE の統合）も関連。訓練は非常に困難だが、LLM 内部理解に有望。

> [!abstract]- ユースケース①：クレジットセンチメント分析（Sentiment Feature）
>
> 背景：2017年、OpenAI が LSTM 訓練中に Amazon レビューのセンチメントを担う**たった1つのニューロン**を発見。モデル全体を除去してもそのニューロンだけでセンチメントが機能した。これが本研究の動機。
>
> **手順**：
> 1. Neuronpedia プラットフォームで Llama 3（8B）に SAE をロードし "credit risk" で検索
> 2. "Financial risk and issues related to credit payments and financial terms" 等の関連特徴量を特定
> 3. クレジット関連特徴量の活性化を増幅（**ステアリング**）
>
> **結果**：同じ文・同じプロンプトで、ステアリングなし → センチメント評価 2/10、ステアリングあり → 4/10。モデルは "lower credit score", "secured financial", "reduced debt" 等のクレジット固有概念に集中。
>
> > One very important thing to note here is that there is no prompting, there is no fine tuning we did, it was just the result of steering the model.
>
> **Ariye（実応用）**: 事前ラベル付きニュースセンチメントデータで検証。ステアリング前後の Confusion Matrix を比較し、クレジットリスクセンチメントの精度が向上。汎用センチメントからクレジット特化への調整がステアリングだけで実現。

> [!abstract]- ユースケース②：Warren Buffett AI（トレーディングシグナル抽出）
>
> **Hariom**: LLM の脳には株式市場の歴史、価格アノマリー、サブプライム危機、COVID、マクロレジームシフト、ボラティリティパターン、さらには衛星画像情報まで内包されている可能性がある。その「針」を見つけ出すのが目標。
>
> **訓練パイプライン**：
> 1. 過去10年・10,000件以上の金融ニュースヘッドラインを SAE（モデル: Gemma 2）に通す
> 2. 10,000+ の特徴量から、金融ニュースで頻繁に活性化する約300特徴量を選定
> 3. 特徴量活性化値を入力、S&P500/Apple の価格変動（上/下）をラベルとして **Random Forest** を訓練
>
> **特徴量重要度の結果**：
> 1. Names of places / Location（**Named Entity Recognition** — 金融 NLP で既知の重要特徴量と合致）
> 2. Financial terms
> 3. Stock ticker symbols and finance-related abbreviations
> 4. （一部スプリアス相関：car and vehicle related terms）
>
> > The results were very, very intuitive, especially the first one, which was named entity recognition or the NER feature. So really great outcome.

> [!abstract]- ユースケース③：Hallucination Police（ハルシネーション抑制）
>
> 既存のハルシネーション対策（プロンプティング、ガードレール、参照、推論モデル、Human-in-the-loop）に加え、LLM 内部から抑制するアプローチ。
>
> **ワークフロー**：
> 1. 金融関連の文・フレーズから SAE で金融特化の特徴量を20-30個選定
> 2. 質問入力時に SAE で特徴量活性化を計算
> 3. 活性化 > 閾値（例：20%）→ そのまま出力
> 4. 活性化 < 閾値 → **プロンプト拡張**（SEC ファイリング等の追加コンテキストを自動注入）
>
> **結果例**（8-K 提出期限の質問）：
> - 条件チェックなし → "typically within four business days of the event"（短い回答）
> - 条件チェックあり → 4営業日に加え、例外項目・セクション別の逸脱・SEC 規則の引用まで出力
>
> > Really good output, no hallucination or less hallucination and really grounded one.

> [!abstract]- 今後の研究：古典ファクター拡張 & エージェント監視
>
> **古典ファクターの拡張**（Warren Buffett AI の発展）：
>
> 従来のファクター（S&P500リターン、ボラティリティ、ヒストリカルデータ、ニュースセンチメント）に、LLM 内部特徴量（insider buying, earning misses, analyst blog commentary, M&A deal flow 等）を追加。
>
> > When we moved from rule-based modeling to statistical technique, we augmented it with statistical and machine learning technique. Now the idea can be moved to the next step, augmenting those statistical technique with all these features.
>
> **エージェント監視（Agentic Monitoring）**（Ariye）：
>
> > Agents even raises more of a stakes because now you're letting AI make decisions. We are looking into the way to monitor agent reasoning during execution of the workflow steps. We're using feature activations and live diagnostic signal that something might be wrong with an agent or something wrong with execution.
>
> 具体例：エージェントがデータベースに誤ったクエリを実行 → SAE で実行中にライブ検出し、停止または修正。コスト削減にも寄与（トークン消費の最適化）。

> [!abstract]- 技術スタック・制約・最終見解
>
> **技術スタック**: PyTorch + NVIDIA CUDA、NVIDIA Launchpad（H100 GPU × 8 にリモートアクセス）
>
> **制約**：
> - オープンウェイトモデルが必須。クローズドモデルの内部は観察不可。代替策としてベンダーに解釈可能性ツールの提供を求めるべき
> - 現時点では単一層の解析に限定。Circuits（多層解析）は訓練が非常に困難
> - 計算コストが高い（Cross-coder の訓練、全層の SAE 等）
> - 解釈可能性の定量的メトリクスが未成熟
>
> **最終見解**：
>
> > Still we feel that mechanistic interpretability, looking inside the model, might be underrated, especially in high-stake domain like finance. And we think that this is something which should be must-have in finance and also high-stakes domain.
>
> > 85% of the use cases are still stuck in POC state. Knowing deeper or getting insight into the models might unlock and give us confidence so that we are able to even unlock new use cases and scale adoption across our industry.
>
> > If we understand the model really well inside out, it might help us avoid one of the financial crisis going forward.

## 当チームへの示唆

- **センチメント分析の高度化**：Feature Steering により、汎用 LLM をファインチューニングなしでドメイン特化のセンチメント分析器に調整できる。クレジットリスクや市場センチメント分析への応用可能性が高い
- **トレーディングシグナルの新たなソース**：LLM 内部特徴量を古典的ファクターと組み合わせるアプローチは、当チームの投資戦略開発に新しい切り口を提供する
- **ハルシネーション対策**：金融チャットボットや社内 AI ツール構築時に、SAE ベースの条件付きプロンプト拡張は実用的なハルシネーション低減策として検討に値する
- **モデルリスク管理への貢献**：MechInterp はモデル検証・監査の新たな手法として、規制対応やモデルガバナンス強化に直結する
- **エージェント監視**：当チームが AI エージェントを業務に導入する際、SAE による実行時監視はガバナンスとコスト管理の両面で有用
