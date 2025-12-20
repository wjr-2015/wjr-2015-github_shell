from github_shell.utils.request_utils import GitHubRequest
from github_shell.utils.config import USERNAME
from github_shell.utils.language import _

class UserCommands:
    """用户命令处理类"""
    
    def __init__(self):
        self.request = GitHubRequest()
    
    def show_user(self, username, output_format="print"):
        """查看指定用户信息"""
        user = self.request.send_request(f"/users/{username}")
        result = {}
        
        if user:
            result = {
                "name": user['name'] or user['login'],
                "company": user['company'] or '无',
                "location": user['location'] or '无',
                "followers": user['followers'],
                "following": user['following'],
                "public_repos": user['public_repos']
            }
        
        if output_format == "print":
            print(_("user_info", username))
            print(_("repo_name", result['name']))
            print(_("user_company", result['company']))
            print(_("user_location", result['location']))
            print(_("user_followers", result['followers']))
            print(_("user_following", result['following']))
            print(_("user_repos", result['public_repos']))
        
        return result
    
    def list_followers(self, output_format="print"):
        """查看当前用户的关注者"""
        followers = self.request.send_request(f"/users/{USERNAME}/followers")
        result = [follower['login'] for follower in followers[:10]]  # 只显示前10个
        
        if output_format == "print":
            print(_("user_followers_list", USERNAME))
            for follower in result:
                print(_("branch_format", follower))
        
        return result
    
    def list_following(self, output_format="print"):
        """查看当前用户关注的人"""
        following = self.request.send_request(f"/users/{USERNAME}/following")
        result = [user['login'] for user in following[:10]]  # 只显示前10个
        
        if output_format == "print":
            print(_("user_following_list", USERNAME))
            for user in result:
                print(_("branch_format", user))
        
        return result
