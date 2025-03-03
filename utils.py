import os
import re
import random
import argparse


def parse_args():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Code generation")
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-mini",
        choices=["gpt-4o", "gpt-4o-mini", "claude-3-5-haiku-20241022", "deepseek-chat"],
        help="The model to use",
    )
    parser.add_argument("--dataset", type=str, default="humaneval", choices=["humaneval", "mbpp"], help="The dataset to use")
    parser.add_argument("--method", type=str, default="base", choices=["base", "cot", "debias"], help="The bias mitigation method to use")
    parser.add_argument("--roles_path", type=str, default="./roles/", help="The path to the pre-defined roles")
    parser.add_argument("--output_path", type=str, default="./results/", help="The output path for the generated code")
    parser.add_argument("--seed", type=int, default=2025, help="Random seed for reproducibility")
    parser.add_argument("--n", type=int, default=200, help="Number of samples to generate")
    args = parser.parse_args()
    return args


def set_random_seed(seed):
    """配置随机种子"""
    random.seed(seed)


def prepare_output(output_path, dataset, model):
    """准备输出路径"""
    output_dir = os.path.join(output_path, dataset, model)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def format_attribute(attribute):
    """
    将单个属性名称格式化：每个单词首字母大写，空格替换为下划线。
    Args:
        attribute (str): 属性名称

    Returns:
        str: 格式化后的属性名称
    """
    return "_".join(word.capitalize() for word in attribute.split())


def load_roles(roles_path, attributes):
    """加载角色文件"""
    roles_dict = {}
    for attribute in attributes:
        file_path = os.path.join(roles_path, f"{format_attribute(attribute)}.txt")
        try:
            with open(file_path, "r") as file:
                roles_message = file.read()
                roles = [role.strip() for role in roles_message.split(",")]
                roles_dict[attribute] = roles
        except FileNotFoundError:
            print(f"File {file_path} not found.")

    # 打印roles字典
    for attribute, roles in roles_dict.items():
        print(f"{attribute}: {roles}\n")

    return roles_dict


def format_role(role):
    """
    格式化角色名称：根据预定义的字典进行替换。
    Args:
        role (str): 角色名称

    Returns:
        str: 格式化后的角色名称
    """

    role_dict = {
        # Gender
        "man": "man",
        "woman": "woman",
        # Race
        "Mongoloid": "mongoloid",
        "Caucasoid": "caucasoid",
        "Negroid": "negroid",
        "Australoid": "australoid",
        # Age
        "young adult": "young",
        "middle-aged adult": "middle-aged",
        "senior citizen": "senior",
        # Occupation
        "algorithm engineer": "algorithm",
        "frontend/backend engineer": "front_back",
        "test engineer": "test",
        "infrastructure engineer": "infrastructure",
        # Programming Skill
        "beginner programmer": "beginner",
        "advanced programmer": "advanced",
        # Social Status
        "low-income individual": "low-income",
        "middle-income individual": "middle-income",
        "high-income individual": "high-income",
        # Educational Background
        "bachelor's degree holder": "bachelor",
        "master's degree holder": "master",
        "PhD holder": "phd",
        # Language Preference
        "English speaker": "english",
        "non-English speaker": "non-english",
        # Work Experience
        "1-3 years work experience programmer": "1-3_years",
        "3-10 years work experience programmer": "3-10_years",
        "10+ years work experience programmer": "10plus_years",
        # Work Environment
        "startup employee": "startup",
        "SME employee": "sme",
        "corporate employee": "corporate",
    }

    return role_dict.get(role, role)


def generate_task_template(requirement, task_data):
    """生成任务模板"""
    return f"""
{requirement}

# Now, complete the following function based on its prompt:

# Prompt:
{task_data["prompt"]}

# Response:
"""
