import json
from github import Github
import Github_get_started as git_start
from MailFiles import send_mail

class Git(object):          #named Git to avoid name conflicts

    all_repo = git_start.getAllRepo()
    user = git_start.getUser()

    def __init__(self, access_token):
        self.git = Github(access_token)
        self.output = ""
        self.mail_body = dict()

    def searchRepoByLanguage(self, **args):
        lan = args["language"]
        try:
            foundRepos = list()
            for repo in self.git.get_user().get_repos():
                if repo.language == lan:
                    # print(repo.name)
                    foundRepos.append(repo.name)
            if foundRepos:
                self.output = "The repositories in language " + lan + " are: " + " ".join(map(str, foundRepos))
                self.mail_body.update({'Repo name':foundRepos})
                # print(self.mail_body)
                # print(self.output)
                send_mail.sendMail(self.mail_body)
            else:
                self.output = "No such repository found."
        except:
            self.output ="Error in getting the information"
        # speak.say(self.output)
        return self.output
        
    def listOfOpenIssues(self, **args):
        reponame = args["repo name"]
        try:
            repo = self.git.get_user().get_repo(reponame) 
            open_issues = repo.get_issues(state='open')
            openiss=list()
            for issue in open_issues:
                openiss.append(issue)
            if openiss:
                self.output = "The open issues are: "+" ".join(map(str, openiss))
                self.mail_body.update({'Issues':openiss})
                send_mail.sendMail(self.mail_body)
            else:
                self.output = "No issues found"
        except:
            self.output="Error in getting the information"
        # speak.say(self.output)
        return self.output
        

    def getLabelsOfRepo(self, **args):
        reponame = args["repo name"]
        try:
            repo = self.git.get_user().get_repo(reponame) 
            labels = repo.get_labels()
            lab=list()
            for label in labels:
                lab.append(label.name)
            if lab:
                self.output = "The labels are: "+" ".join(map(str, lab))
                self.mail_body.update({'Issues':lab})
                send_mail.sendMail(self.mail_body)
            else:
                self.output = "No labels found"
        except:
            self.output="Error in geeting the information"
        # speak.say(self.output)
        return self.output

    def searchRepoWithGoodFirstIssue(self, **args):
        try:
            repositories = self.git.search_repositories(query='good-first-issues:>3')
            gfissue=list()
            for i, repo in enumerate(repositories):
                # print(repo.name)
                gfissue.append(repo.name)
                if gfissue:
                    self.output = "The repositories with good first issue are: "+" ".join(map(str, gfissue))
                    self.mail_body.update({'Issues':gfissue})
                else:
                    self.output = "No issues found"
                if i==10:               #10 repo only
                    break
            send_mail.sendMail(self.mail_body)
        except:
            self.output="Error in getting the information"
        # speak.say(self.output)
        return self.output

    def getAllContentsOfRepo(self, **args):
        reponame = args["repo name"]
        try:
            repo = self.git.get_user().get_repo(reponame) 
            contents = repo.get_contents("")
            cont=list()
            for content_file in contents:
                # print(content_file.path)
                cont.append(content_file.path)
            if cont:
                self.output = "The contents of the repo are: "+" ".join(map(str, cont))
                self.mail_body.update({'Issues':cont})
                send_mail.sendMail(self.mail_body)
            else:
                self.output = "No labels found"
        except:
            self.output="Error in geeting the information"
        # speak.say(self.output)
        return self.output

    def createNewRepo(self, **args):
        reponame = args["repo name"]
        try:
            self.git.get_user().create_repo(reponame)
            self.output="Successfully created."
            self.mail_body={
                "Repo name":reponame
            }
            send_mail.sendMail(self.mail_body)
        except:
            self.output = "Error in creating repository."
        # speak.say(self.output)
        return self.output

    def createNewFileInRepo(self, **args):
        reponame = args["repo name"]
        filename = args["file name"]
        description = "This is the default description given by IPM"
        commit = "Added a file {0} by IPM".format(filename)
        try:
            repo = self.git.get_user().get_repo(reponame)               #to avoid passing username, use get_user()
            repo.create_file(filename, commit, description)
            self.output="Successfully created the file."
            self.mail_body={
                "Repo name":reponame,
                "File Name":filename,
                "Commit Message":commit,
                "Description":description
            }
            send_mail.sendMail(self.mail_body)
        except:
            self.output="Error in creating the file"
        # speak.say(self.output)
        return self.output

    def deleteFileFromRepo(self, **args):
        reponame = args["repo name"]
        filename = args["file name"]
        try:
            repo = self.git.get_user().get_repo(reponame)  
            contents = repo.get_contents(filename)
            repo.delete_file(contents.path, "removed "+filename, contents.sha)
            self.output="Successfully deleted the file."
            self.mail_body={
                "Repo name":reponame,
                "File Name":filename,
                "Commit Message":"removed the file"
            }
            send_mail.sendMail(self.mail_body)
        except:
            self.output="Error in deleting the file"
        # speak.say(self.output)
        return self.output

    def getLatestCommitDateOfUser(self, **args):
        try:
            author=self.git.get_user().login
            commits = self.git.search_commits(query = 'author:'+author+' sort:author-date-desc')
            data = commits.get_page(0)
            cdate=str(data[0].commit.committer.date)
            self.output ="The latest commit date is "+ cdate
            self.mail_body={
                "Latest Commit date":cdate
            }
            send_mail.sendMail(self.mail_body)
        except:
            self.output="Error in getting the details"
        # speak.say(self.output)
        return self.output
    
    # ==================================================================================
        # PULL REQUEST        NOT WORKING 
    # ====================================================================================
    # def createANewPullRequest(self,reponame,title1,body1):
    #     repo = self.git.get_user().get_repo(reponame)
    #     pr = repo.create_pull(title = title1, body = body1, head='')
    # ====================================================================================

    def createNewIssue(self, **args):
        reponame = args["repo name"]
        title = args["title"]
        try:
            repo = self.git.get_user().get_repo(reponame)
            repo.create_issue(title=title)
            self.output="Successfully created the issue."
            self.mail_body={
                "Repo name":reponame,
                "title":title
            }
            send_mail.sendMail(self.mail_body)
        except:
            self.output = "Error in creating the issue."
        # speak.say(self.output)
        return self.output

    def createIssueWithBody(self, **args):
        reponame = args["repo name"]
        title = args["title"]
        body = args["body description"]
        try:
            repo = self.git.get_user().get_repo(reponame)
            repo.create_issue(title=title, body=body)
            self.output="Successfully created the issue."
            self.mail_body={
                "Repo name":reponame,
                "title":title,
                "body":body
            }
            send_mail.sendMail(self.mail_body)
        except:
            self.output = "Error in creating the issue."
        # speak.say(self.output)
        return self.output

    def createIssueWithLabel(self, **args):
        reponame = args["repo name"]
        title = args["title"]
        labels = args["label"]
        try:
            repo = self.git.get_user().get_repo(reponame)
            label = repo.get_label(labels)
            repo.create_issue(title=title, body=body, labels=[label])
            self.output="Successfully created the issue."
            self.mail_body={
                "Repo name":reponame,
                "title":title,
                "body":body,
                "labels":labels
            }
            send_mail.sendMail(self.mail_body)
        except:
            self.output = "Error in creating issue."
        # speak.say(self.output)
        return self.output
        
    def getIssueByNumber(self, **args):
        reponame = args["repo name"]
        issue_number = int(args["issue number"])
        try:
            repo = self.git.get_user().get_repo(reponame)
            iss=repo.get_issue(number=issue_number)
            # print(iss.title)
            self.output="The issue is "+iss.title
            self.mail_body={
                "Repo name":reponame,
                "Issue number":issue_number,
                "issue":iss.title
            }
            send_mail.sendMail(self.mail_body)
        except:
            self.output = "Error in getting the issue."
        # speak.say(self.output)
        return self.output
    def closeIssueByNumber(self, **args):
        reponame = args["repo name"]
        issue_number = int(args["issue number"])
        repo = self.git.get_user().get_repo(reponame)
        open_issue = repo.get_issue(number=issue_number)
        open_issue.edit(state='closed')
        self.output="The issue is closed"
        self.mail_body={
            "Repo name":reponame,
            "Issue number":issue_number,
            "issue state":"closed"
        }
        send_mail.sendMail(self.mail_body)
        # speak.say(self.output)
        return self.output

    def closeAllOpenIssues(self, **args):
        reponame = args["repo name"]
        try:
            repo = self.git.get_user().get_repo(reponame)
            open_issues = repo.get_issues(state='open')
            for issue in open_issues:
                issue.edit(state='closed')
            self.output="All the issues are closed"
            self.mail_body={
                "Repo name":reponame,
                "issue state":"All issues are closed"
            }
            send_mail.sendMail(self.mail_body)
        except:
            self.output = "Error in closing the issues."
        # speak.say(self.output)
        return self.output



