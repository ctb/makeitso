def find_cwldef(taskname):
    if taskname.startswith('http'):
        url = taskname
    else:
        # try repo/path:tag
        user, path = taskname.split('/', 1)

        if '/' in path:
            repo, path = path.split('/', 1)
        else:
            repo = path
            path = ''

        branch = 'master'
        if ':' in path:
            path, branch = path.rsplit(':', 1)
        elif path is '':
            if ':' in repo:
                repo, branch = repo.rsplit(':', 1)

        if path == '':
            path = 'Dockstore.cwl'        # hack

        github_url = 'https://raw.githubusercontent.com/{}/{}/{}/{}'
        url = github_url.format(user, repo, branch, path)

    return url
