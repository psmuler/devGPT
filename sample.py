from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import os

os.environ["OPENAI_API_KEY"] = "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"

# チャットモデル gpt-3.5-turboを使う
llm = ChatOpenAI(temperature=0, max_tokens=200)

ai1_name = "developer"
ai2_name = "repository"

ai1_prefix = """あなたの名前はdeveloperです 。
あなたはプロの技術者です。repositoryが持っている情報を参照しながら求められたスプリントゴールを達成するために必要なコードや実装を提案してください。
わからない場合はrepositoryに聞いてください。ただし、repositoryに聞きたい内容は[]でくくってください
例：[第一スプリントゴールを教えてください]


Current conversation:
{history}
repository:{input}
developer:
"""

# プレフィックス
ai2_prefix = """あなたの名前はrepositoryです。developerと一緒にアプリ開発を進めています。
あなたはgithubのレポジトリです。developerから現在の仕様を聞かれたらdocumentの中から適切な部分を抽出して説明してください。
ただしdeveloperが聞きたい内容は全て[]内に記載されているので、それ以外の部分は無視して構いません。
それを元により適切な実装のために詳しく聞いてほしい部分を聞いてください。

Current conversation:
{history}
developer:{input}
repository:
"""


# chatプロンプトテンプレート
prompt1 = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(ai1_prefix),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

prompt2 = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(ai2_prefix),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

# メモリ
memory1 = ConversationBufferMemory(
    return_messages=True
)
memory2 = ConversationBufferMemory(
    return_messages=True
)

# 会話チェーン
conversation1 = ConversationChain(
    memory=memory1, 
    prompt=prompt1, 
    llm=llm
)
conversation2 = ConversationChain(
    memory=memory2, 
    prompt=prompt2, 
    llm=llm
)


ai1_says = "[第一のスプリントゴールを教えてください。]"
print(ai1_name, ":", ai1_says)

for i in range(2):
  ai2_says = conversation2.predict(input=ai1_says)
  print(ai2_name, ":", ai2_says)
  ai1_says = conversation1.predict(input=ai2_says)
  print(ai1_name, ":",ai1_says)