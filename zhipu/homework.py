from typing import Generator, List, Dict
from zhipuai import ZhipuAI

API_KEY = ""
client = ZhipuAI(api_key=API_KEY)

def generate_role_appearance(role_profile: str) -> Generator[str, None, None]:
    instruction = f"""
请从下列文本中，抽取人物的性格描写，要求： 
1. 只生成性格描写，不要生成任何多余的内容。
2. 性格描写不能包含敏感词，人物形象需得体。
3. 尽量用短语描写，而不是完整的句子。
4. 不要超过50字
5. 输出格式：我是「角色名」，我的性格是「性格描写」

文本：
{role_profile}
"""
    return get_chatglm_response(
        messages=[
            {
                "role": "user",
                "content": instruction.strip()
            }
        ]
    )

def get_chatglm_response(messages: List[Dict[str, str]]) -> Generator[str, None, None]:
    response = client.chat.completions.create(
        model="glm-4",
        messages=messages
    )
    return response.choices[0].message.content

def generate_role_profile(description: str) -> str:
    """
    generate user profile from description
    """
    return generate_role_appearance(description)



def generate_response(message_history: List[Dict[str, str]]) -> str:
    # Call the API to generate a response
    response = client.chat.completions.create(
        model="charglm-4",
        messages=message_history
    )
    # Extract the assistant's response from the API response
    return response.choices[0].message.content

def generate_conversation(user1_name: str, user1_profile: str, user2_name: str, user2_profile: str, initial_message: str, rounds: int):
    # Initialize the message histories for both user1 and user2
    user1_history: List[Dict[str, str]] = [
        {"role": "system", "content": user2_profile}
    ]
    user2_history: List[Dict[str, str]] = [
        {"role": "system", "content": user1_profile}
    ]

    # Start with the initial message for user1
    user1_message = initial_message

    for _ in range(rounds):
        # Add user1's message to chat1 history
        user1_history.append({"role": "user", "content": user1_message})

        # Generate user2's response based on chat1 history
        user2_response = generate_response(user1_history)

        # Add user2's response to chat2 history
        user2_history.append({"role": "user", "content": user2_response})

        # Print the conversation from user1 to user2
        print(f"{user1_name}:", user1_message)
        print(f"{user2_name}:", user2_response)

        # Generate user1's next message based on user2 history
        user1_message = generate_response(user2_history)

def main():
    user1_name = "张伟"
    user2_name = "李娜"
    
    user1_description = f"{user1_name}是一位热爱科学的高中生，尤其对物理和化学充满了浓厚的兴趣。他总是积极参加学校的科学竞赛，并在其中屡获佳绩。张伟喜欢在课余时间阅读科普书籍，并梦想着未来成为一名科学家。他的朋友们都称赞他为'科学小达人'。"
    user2_description = f"{user2_name}是一位充满创意的高中生，擅长绘画和写作。她的作品曾多次在校内外的比赛中获奖。李娜喜欢用画笔和文字表达自己的情感和想法，她希望将来能成为一名作家或插画师。她的同学们都很欣赏她的艺术才华。"

    user1_profile = generate_role_profile(user1_description)
    user2_profile = generate_role_profile(user2_description)

    print(user1_profile)
    print(user2_profile)

    initial_message = f"你好，我是{user1_name}，很高兴认识你。"
    rounds = 3

    generate_conversation(user1_name, user1_profile, user2_name, user2_profile, initial_message, rounds)

if __name__ == "__main__":
    main()

