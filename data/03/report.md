---
title: "Build High-Performance Financial AI: Achieve Microsecond Latency and Scalable LLM Inference"
author: inu
created: 2026-03-18
tags:
  - NVIDIA-GTC-2026
  - low-latency-inference
  - LSTM
  - RAG
  - GPU-optimization
---

## 会議情報

| 項目 | 内容 |
| --- | --- |
| カンファレンス | NVIDIA GTC 2026 |
| 日時 | 2026年3月18日（水）1:00 - 1:40 JST |
| 講演者 | Martin Marciniszyn Mehringer（Sr. AI DevTech Manager, NVIDIA）、Nikolai Markovskii（Sr. AI DevTech Engineer, NVIDIA） |
| トピック | Developer Tools & Techniques - AI Inference |

## 全体まとめ

NVIDIA の DevTech チームが、金融業界の標準ベンチマーク **STAC-ML**（LSTM 推論）と **STAC-AI**（RAG 推論）における最適化実装と性能結果を発表したセッション。

前半では、時系列予測（価格予測）を想定した LSTM 推論において、スライディングウィンドウの事前計算バッチ化とパーシステントカーネルにより **4.7マイクロ秒**（LSTM-A）という超低レイテンシを Grace Hopper Superchip 上で達成。FPGA 競合と同等以上の性能を GPU で実現した。

後半では、RAG 推論（Llama 3.1 8B/70B + Edgar ファイリングデータ）のベンチマークにおいて、Grace Blackwell が GH200 比で約2倍のスループットを達成。MBFP4 量子化の効果が大きい。実装には TensorRT-LLM を使用し、コードやベンチマーク再現手順の公開も予定されている。

## Key Points

### 1. STAC-ML ベンチマーク — LSTM 推論（時系列予測）

| モデル | パラメータ数 | FLOPs | レイテンシ（GH200） |
| --- | --- | --- | --- |
| LSTM-A（小） | 160K | 16.1M | **4.7 μs** |
| LSTM-B（中） | 1M | 200M | **7.1 μs** |
| LSTM-C（大） | 30M | 6B | FPGA 比約2倍高速 |

- ベンチマークはホスト上でのデータ受信からデバイスへの転送、推論、結果返却までを計測（wire-to-wire）
- ベースラインの wire-to-wire レイテンシ：x86+H200 で約3μs、GH200 で約2.3μs → LSTM-A の 4.7μs のうち半分以上が通信コスト
- 6倍低いアウトライア（外れ値）を達成 → ワークロードの安定性・予測可能性が高い

### 2. 核心技術 — スライディングウィンドウ最適化

- **基本アイデア**：新しい入力 x_t を受信した時点で、その入力が将来の K 個のウィンドウ全てに寄与する分を事前計算
- **効果**：行列-ベクトル積 → **行列-行列積**に変換（GPU に最適なバッチ演算）
- 移動平均の差分計算に類似するが、LSTM のゼロ初期化制約により追加の工夫が必要

### 3. パーシステントカーネルによる低レイテンシ実装

- LSTM の重み行列 W を GPU の**共有メモリ（Shared Memory）に事前ロード**
- デバイスメモリへのアクセスを完全に回避
- 常時稼働するパーシステントカーネルが新入力をブロードキャスト → ローカル行列-ベクトル積 → SM 間ギャザー → 出力
- モデルサイズ別の実装戦略：
  - **LSTM-A（小）**：単一 SM で完結 → SM 間同期不要で最速
  - **LSTM-B（中）**：Thread Block Cluster（Hopper 以降）で分散共有メモリ同期
  - **LSTM-C（大）**：188 SM 中 184 SM を使用、グローバルメモリ経由の同期（約2μs）

### 4. STAC-AI ベンチマーク — RAG 推論

| 構成 | モデル | データセット | 入出力トークン数 |
| --- | --- | --- | --- |
| 構成1 | Llama 3.1 8B | Edgar 4 | ~2,000 in / 250 out |
| 構成2 | Llama 3.1 8B | Edgar 5 | ~60,000 in / 500 out |
| 構成3 | Llama 3.1 70B | Edgar 4 | ~2,000 in / 250 out |
| 構成4 | Llama 3.1 70B | Edgar 5 | ~60,000 in / 500 out |

- **Grace Blackwell（GB200）**：GH200 比で約2倍のスループット（per GPU）。MBFP4 量子化が主要因
- **RTX Pro 6000 Blackwell**：HBM 非搭載のためスループットは劣るが、コロケーション環境でのデプロイに適する
- 実装は **TensorRT-LLM** + **Model Optimizer**（量子化・キャリブレーション）

### 5. ハードウェアとデプロイ構成

| ハードウェア | 特徴 |
| --- | --- |
| **Grace Hopper Superchip（GH200）** | 大容量高速メモリ、チップ間高速接続、ARM CPU 併載 |
| **Grace Blackwell（GB200）** | MBFP4 対応、GH200 比2倍スループット |
| **RTX Pro 6000 Blackwell** | コロケーション向け、水冷/空冷の8GPU サーバー構成等 |

- GDR Copy（GPU Direct）によるレイテンシ低減
- コード公開：GitHub 上の `nvidia-dl-low-latency` リポジトリ（Docker ビルド対応）

## 講演ノート（トランスクリプト）

> [!abstract]- イントロダクション — AI と金融市場
>
> **司会**: Martin comes from an organization at NVIDIA we call DevTechs, aka we also call them CUDA Ninjas. So you'll hear all of the best practices when it comes to squeezing out maximum performance.
>
> **Martin**: AI is reshaping capital markets. It helps us to deal with complex data, it helps us to predict markets, to predict price moves in markets, and it helps us to improve our execution strategies in financial markets.
>
> 本セッションでは2つの金融業界標準ベンチマークの実装を紹介：
> - **STAC-ML** — LSTM 推論（時系列予測）
> - **STAC-AI** — RAG 推論

> [!abstract]- STAC とは何か
>
> STAC = Strategic Technology Analysis Center。金融業界の技術評価組織。
>
> > When STAC defines a benchmark, we have a council of vendors, but also financial clients, banks, trading companies who come together to define a benchmark. STAC defines the exact benchmark rules and conducts the audit. Vendors like us submit our implementation.
>
> STAC のニュースレターに登録すると、全ベンチマーク結果が定期公開される。

> [!abstract]- STAC-ML ベンチマーク — LSTM 推論の概要
>
> 入力：k 個のタイムステップ × n 次元ベクトル → 多層 LSTM ネットワーク → 出力ベクトル y_t → 重み付き和でスカラー出力。ベンチマークはこのスカラーの精度を検証。
>
> 3つのモデルサイズ：
> - **LSTM-A**：160K パラメータ、16.1M FLOPs
> - **LSTM-B**：1M パラメータ、200M FLOPs
> - **LSTM-C**：30M パラメータ、6B FLOPs
>
> 2つのベンチマークスイート：
> - **Sumaco** — 毎回完全に新しいランダム入力
> - **Takana** — スライディングウィンドウ（最古の入力を除去、最新を追加）
>
> タイマーは「ホスト上でデータ受信 → デバイスへ転送 → 推論 → 結果をホストに返却」の全体を計測。

> [!abstract]- LSTM セルの数学的構造
>
> LSTM セルのパラメータ：W 行列（新入力用）と U 行列（前の隠れ状態用）。
>
> > The dominant operations that we want to accelerate are the matrix vector multiplications. In particular the matrix vector multiplication between W and x_t. The U multiplication with the previous hidden state can be pre-computed — it is already known at the time when we receive new input.
>
> 多層 LSTM の評価：左下から波面状に隠れ状態を上方・右方に伝播。最終的に右上で出力ベクトルを取得。

> [!abstract]- スライディングウィンドウ最適化 — 行列-行列積への変換
>
> > When you receive your newest input x_t, you know that this input will contribute not only to the LSTM inference that you want to compute now, but also to the window that will follow next and the window after that. So x_t will have contributions to K sliding windows and we can compute these contributions already at the time when we receive x_t.
>
> 移動平均のアナロジー：新しい値を加え古い値を引く。ただしベンチマーク規則で最古の隠れ状態はゼロ初期化が必要なため追加の工夫が必要。
>
> **効果**：行列-ベクトル積 → 行列-行列積のバッチ演算に変換。GPU の全計算ユニットを活用可能に。

> [!abstract]- ベンチマーク結果の歴史と FPGA との比較
>
> | 年 | 提出者 | LSTM-A | LSTM-B | LSTM-C | 備考 |
> | --- | --- | --- | --- | --- | --- |
> | 2022 | NVIDIA（初回） | 29 μs | 58 μs | 620 μs | A100 |
> | 2023 | Myrtle（FPGA） | — | — | — | NVIDIA のバッチ化手法を採用、事前計算をタイム外に |
> | 2024 | NVIDIA（最新） | **4.7 μs** | **7.1 μs** | FPGA 比約2倍高速 | GH200、パーシステントカーネル |
>
> > We had very low latencies, which is often surprising that you can get these low latencies on GPUs. This is not something that people typically expect. The maximum outliers were very small — very predictable and very stable workload. Lower inference errors and very energy efficient.

> [!abstract]- パーシステントカーネルの実装詳細
>
> 1. LSTM の重み行列 W を各 SM の**共有メモリに事前ロード**（デバイスメモリアクセス回避）
> 2. 新入力 x_t を全 SM にブロードキャスト
> 3. 各 SM でローカル行列-ベクトル積を計算
> 4. SM 間ギャザー操作（最もコストの高い同期処理）
> 5. 次の層も同様に処理し最終出力を生成
>
> モデルサイズ別の実装：
> - **LSTM-A**：1 SM で完結。SM 内同期のみで最も高速
> - **LSTM-B**：Thread Block Cluster（Hopper）で分散共有メモリ同期
> - **LSTM-C**：188 SM 中 184 SM を使用。グローバルメモリ同期に約2μs
>
> Wire-to-wire レイテンシ下限：x86+H200 で約3μs、GDR Copy 使用で改善、GH200 で約2.3μs。
>
> コード公開済み：GitHub の `nvidia-dl-low-latency`（Docker ビルド対応、RTX Pro 6000 Blackwell 向けに設計）

> [!abstract]- STAC-AI ベンチマーク — RAG 推論
>
> RAG パイプラインの推論ステージのみに焦点。
>
> 使用モデル：Llama 3.1 8B、Llama 3.1 70B
> データセット：Edgar 4（~2K tokens in, 250 out）、Edgar 5（~60K tokens in, 500 out）
>
> **スループット結果**（per GPU）：
> - **GH200**：完全監査済み（HPE と共同）。ベースライン
> - **Grace Blackwell（GB200）**：GH200 比約2倍。MBFP4 量子化による効果が主因。Nebius と共同で STAC Vault に提出
> - **RTX Pro 6000 Blackwell**：メモリ帯域の制約でスループットは劣るが、コロケーション向けに有利。Red Hat + Supermicro + OpenShift で監査中
>
> > When you go to Blackwell, you see roughly twice the performance compared to Grace Hopper. And this is per GPU. The gains come mostly from using MBFP4, which is available on Blackwell but not on Hopper.
>
> 実装は TensorRT-LLM。NGC からイメージ取得 → Model Optimizer で量子化 → キャリブレーション用合成データ生成 → ベンチマーク実行。結果公開後にブログで再現手順を公開予定。
>
> DevTech チームが開発する高速カーネルは **Flash Infer** フレームワークに統合され、TensorRT-LLM だけでなく vLLM、SGLang 等のオープンソース推論エンジンにも提供される。

## 当チームへの示唆

- **低レイテンシ推論の可能性**：GPU で4.7μs の LSTM 推論が可能という結果は、リアルタイム市場データ分析やリスクモデリングの高速化に直結する。FPGA に匹敵する性能が GPU で達成できる点は、開発の柔軟性とコストの観点で重要
- **スライディングウィンドウ最適化**：時系列予測における事前計算バッチ化のテクニック（行列-ベクトル → 行列-行列積への変換）は、当チームの時系列モデルにも応用可能な汎用的な最適化パターン
- **RAG 推論のベンチマーク指標**：STAC-AI のスループット/レイテンシ特性は、当チームが金融文書（Edgar 等）に対する RAG システムを構築する際のハードウェア選定・性能目標の参考になる
- **RTX Pro 6000 Blackwell**：データセンター外（コロケーション）でのデプロイ可能な推論 GPU として、オンプレミス環境での活用を検討する際の選択肢
- **TensorRT-LLM + Model Optimizer**：LLM 推論の量子化・最適化パイプラインとして、当チームの LLM デプロイにも直接活用可能
