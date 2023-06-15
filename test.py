# import requests
# import json
#
# # 确认当前分支和默认分支
# def get_branch_info(repo_owner, repo_name):
#     """
#     获取当前分支和默认分支信息
#     :param repo_owner: 仓库所有者
#     :param repo_name: 仓库名
#     :return: 当前分支名称, 默认分支名称
#     """
#     # 设置认证信息，替换成你自己的GitHub用户名和访问令牌
#     username = 'BrendaWuS'
#     access_token = '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'
#     headers = {'Authorization': f'token {access_token}'}
#
#     # 获取仓库信息
#     repo_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'
#     repo_response = requests.get(repo_url, headers=headers)
#     if repo_response.status_code == 200:
#         repo_data = repo_response.json()
#         default_branch = repo_data['default_branch']
#         print(f'默认分支: {default_branch}')
#
#         # 获取当前分支信息
#         branch_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/branches'
#         branch_response = requests.get(branch_url, headers=headers)
#         if branch_response.status_code == 200:
#             branch_data = branch_response.json()
#             for branch in branch_data:
#                 if branch['name'] == default_branch:
#                     current_branch = branch['name']
#                     print(f'当前分支: {current_branch}')
#                     return current_branch, default_branch
#             print('无法确定当前分支！')
#         else:
#             print('获取分支信息失败！')
#     else:
#         print('获取仓库信息失败！')
#
#     return None, None
#
# # 调用函数来获取当前分支和默认分支信息
# current_branch, default_branch = get_branch_info('BrendaWuS', 'test3')
#################################################


#################################################

import os
import requests
import json

def automate_operations(repo_owner, repo_name, branch_name):
    """
    :param repo_owner: 仓库所有者
    :param repo_name: 仓库名
    :param branch_name: 当前分支名称
    """
    # 设置认证信息，替换成你自己的GitHub用户名和访问令牌
    username = 'BrendaWuS'
    access_token = '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'
    headers = {'Authorization': f'token {access_token}'}

    # 获取当前项目的根目录
    project_directory = os.getcwd()

    # 遍历项目目录，获取所有文件路径
    file_paths = []
    for root, dirs, files in os.walk(project_directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

    # 提交每个文件
    for file_path in file_paths:
        # 读取文件内容
        with open(file_path, 'rb') as file:
            file_content = file.read().decode('utf-8')

        # 提取相对路径
        relative_path = os.path.relpath(file_path, project_directory)

        # 添加修改的文件
        add_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees'
        add_data = {
            'base_tree': branch_name,
            'tree': [
                {
                    'path': relative_path,
                    'mode': '100644',
                    'content': file_content
                }
            ]
        }
        add_response = requests.post(add_url, headers=headers, data=json.dumps(add_data))
        if add_response.status_code == 201:
            tree_sha = add_response.json()['sha']

            # 获取当前分支的最新提交 SHA
            ref_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/heads/{branch_name}'
            ref_response = requests.get(ref_url, headers=headers)
            ref_data = ref_response.json()

            if 'object' in ref_data and 'sha' in ref_data['object']:
                latest_sha = ref_data['object']['sha']
            else:
                print('无法获取当前分支的最新提交 SHA！')
                return

            # 提交更改
            commit_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/git/commits'
            commit_data = {
                'message': 'Automated Commit',
                'tree': tree_sha,
                'parents': [latest_sha]
            }
            commit_response = requests.post(commit_url, headers=headers, data=json.dumps(commit_data))
            if commit_response.status_code == 201:
                commit_sha = commit_response.json()['sha']

                # 推送到远程仓库
                push_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/heads/{branch_name}'
                push_data = {
                    'sha': commit_sha
                }
                push_response = requests.patch(push_url, headers=headers, data=json.dumps(push_data))
                if push_response.status_code == 200:
                    print(f'文件 {relative_path} 自动推送成功！')
                else:
                    print(f'文件 {relative_path} 自动推送失败！')
            else:
                print(f'文件 {relative_path} 自动提交失败！')
        else:
            print(f'文件 {relative_path} 自动添加失败！')

# 调用函数来执行自动化操作
automate_operations('BrendaWuS', 'test3', 'dev')



