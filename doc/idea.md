
Reactor 構想ノート
=======================

2015/02/08　Naoki Tomii

# 目的
------------------------

言論空間の構造化と可視化
民主主義のプラットフォーム構築

# 基本概念
------------------------

## Reaction
Reactorの言論空間は有向重み付きグラフであり、Reactionはそれを構成するノード。以下の項目から構成されるデータ単位を指す。

    * id
    * author：発言者のID
    * time : 発言のタイムスタンプ
    * target : 発言の対象である単一Reactionのid。原則、NULL不可。
    * comment：発言内容。原則、NULLも可。
    * evaluation : target への評価。
      {pros, cons, neutral}のいずれかの値。初期値はneutralで、NULL不可。
    * reactionList :  このReactionをtargetとするReaction idの可変長リスト。初期値blanc
    * reactionFactor : 数値。後述。

twitter のtweetとの差異：

* 基本的に、targetが存在する（後述の"Seed"以外）有向グラフである。

* targetへの評価値であるevaluationが存在する。有向グラフの重みに相当する。

* reactionListが、Reaction Factor（後述）などの再帰的なグラフ解析を可能にする。

## Seed
以下の条件を満たす特殊なReaction。下記Reaction Treeの始点。

    target : NULL
    comment : not NULL

## Reaction Tree

あるSeedから出発し、reactionListを再帰的に探索することで得られるReactionの全体集合。

## Cherry
以下の制約条件を満たす特殊なReaction。下記Reaction Chainの終端。

    reactionList :  blanc

## Reaction Chain

CherryからSeedまでのtarget関係でつながった一連のReaction

## Reaction Factor
あるReactionが、反響を得た程度を定量的に表す数値指標。
あるReactionのFactor値は、Reaction List中の全ReactionのReactionFactorの重み付き合計を使って計算される。
重み付け計算のルールは以下。

* コメントなしCherryのReactionFactor を1.0とする。

* コメントがある方が無いより大きい。

* evaluationの値がprosまたはconsの方がneutralの場合より大きい。

各ReactionのFactorを随時Updateすることで、再帰的にReaction ChainのReaction FactorがUpdateされる。

## Presence
ユーザのReactor内でのコミットメント度合いを示す数値指標。
ユーザがこれまで獲得したReaction Factorの合計。

# UX
_______________

## [Seed] menu
> [Seed] メニューで関心のあるSeedのリストが提示される。キーワードでの検索もできる。

ユーザの関心が高いSeedは、Tree内のReactionのcomment内単語やauthor情報等を使って、過去閲覧したtree との類似度を手がかりに求める。（検索も出来る。）
この指標とSeed の時刻情報（新しい＝Hot ）、さらにSeedのReactionFactorを加味してRecommendation Priorityを決める。

> 興味のあるSeedを選択すると、[Tree]メニューへ移行。

## [Tree] menu
> [Tree]メニューでは、選択したSeedから派生したTree内の探索が出来る。

初期状態はSeedが選択されている。

> あるReactionを選択。
> Pros（賛成）、Cons（反対）、Neutral （中立）ごとにReactionListが表示される。
> キーワードでの絞込み検索も可能
> 興味を引かれたReactionを選択すると、表示が更新される。

表示対象となるReactionの優先度はSeedにおけるRecommendation Priorityと同じ。

> 選択中のReactionに対し、Reaction作成ができる。

Reactionが作成されるとまず、target であるreactionのreactionListに対し、作成されたreactionが登録される。
さらに、targetからSeedに向かってReactionChainを逆向きに、reactionFactorの更新命令が伝播する。

## [Summary] menu
> [Summary] メニューで、Reaction Tree を要約するReaction 集合が表示される。
> Diversity 選択で、複数のSummaryが表示される。

Tree 内の代表的なChainを表示する。
Summary Chain選択アルゴリズムは要検討。

## [Voting] menu
> Seed 作成者はオプションとして、Voting機能を設定することが出来る。
> [Vote] メニューではVote先と、これまでの自分のReactionが表示される。

単純な例では、賛成or反対。

> Reaction TreeにコミットしていないユーザはVoteできない。

コミット度合いの評価にはReaction Factorを使う。

>  「あなたのVote先はもしかして〇〇ですか？」というsuggestionが表示される。
>  Yesを選択してもいいし、無視して好きなVote先を選んでも良い。

これまでVotingを済ませたユーザがいれば、そのユーザとのTree内での相対関係に基づいて
最も尤度の高いVote先をSuggestionする。
最尤推定アルゴリズムも要検討。

> Voting 内容は何度でも変更することが出来る。

## [Account] menu
> これまでの自分の全Reactionが表示される。
> 自分のPresenceのランキングが表示される。

# 運用ルール
_______________

## Seed作成の制限
Seed作成は議題の提出。
Seedが乱立しては、Seedを成長させるReactionを生成するエネルギーが削がれてしまう（まとまりのない議論）。
運営側しか作成できない、またはPresence一定以上のユーザしか作成できないなど、適切な制約が必要だと考えられる。

## 新規Seedの適切な推薦
Seedを成長させるためには、適切に新しいSeedを推薦する必要がある。
Recommendation Priorityの決め方の問題。

## 文字数制限
文字数によって、議論の質が大きく変わると考えられる。短いほどチャットに近くなる。
固定とするか、Seed毎に設定可能とするか。

## 時間制限
あるSeedに対し、Reaction作成やVotingに対する時間制限を設けるか否か。

## 独白の制限
同一authorのReactionをtarget とするReaction作成を制限するか否か。

## 認証済みアカウント
個人情報を元に認証され、個人と紐付けられたアカウント。
たとえばVoting機能設定時に、認証済みアカウントでないと投票できない設定ができれば、Voting結果の信頼性が高まる。
