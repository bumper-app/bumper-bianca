import os
import re
import subprocess
import json
import logging
import math                               # Required for the math.log function
from ingester.commitFile import *         # Represents a file
from classifier.classifier import *       # Used for classifying each commit
from config import REPO_DIRECTORY, config
import time

"""
file: repository.py
authors: Ben Grawi <bjg1568@rit.edu>, Christoffer Rosen <cbr4830@rit.edu>
date: October 2013
description: Holds the repository git abstraction class
"""

class Git():
    """
    Git():
    pre-conditions: git is in the current PATH
                    self.path is set in a parent class
    description: a very basic abstraction for using git in python.
    """
    # Two backslashes to allow one backslash to be passed in the command.
    # This is given as a command line option to git for formatting output.

    # A commit mesasge in git is done such that first line is treated as the subject,
    # and the rest is treated as the message. We combine them under field commit_message

    # We want the log in ascending order, so we call --reverse
    # Numstat is used to get statistics for each commit
    LOG_FORMAT = '--pretty=format:\" CAS_READER_STARTPRETTY\
    \\"parent_hashes\\"CAS_READER_PROP_DELIMITER: \\"%P\\",CAS_READER_PROP_DELIMITER2\
    \\"commit_hash\\"CAS_READER_PROP_DELIMITER: \\"%H\\",CAS_READER_PROP_DELIMITER2\
    \\"author_name\\"CAS_READER_PROP_DELIMITER: \\"%an\\",CAS_READER_PROP_DELIMITER2\
    \\"author_email\\"CAS_READER_PROP_DELIMITER: \\"%ae\\",CAS_READER_PROP_DELIMITER2\
    \\"author_date\\"CAS_READER_PROP_DELIMITER: \\"%ad\\",CAS_READER_PROP_DELIMITER2\
    \\"author_date_unix_timestamp\\"CAS_READER_PROP_DELIMITER: \\"%at\\",CAS_READER_PROP_DELIMITER2\
    \\"commit_message\\"CAS_READER_PROP_DELIMITER: \\"%s%b\\"\
    CAS_READER_STOPPRETTY \" --numstat --reverse '

    CLONE_CMD = 'git clone {!s} {!s}'     # git clone command w/o downloading src code
    PULL_CMD = 'git pull'      # git pull command
    RESET_CMD = 'git reset --hard HEAD'
    CLEAN_CMD = 'git clean -df' # f for force clean, d for untracked directories

    HEAD_COMMIT_HASH_CMD = 'git rev-parse HEAD'

    def getCommitStatsProperties(self, stats, commitFiles, devExperience, author, unixTimeStamp ):
        """
        getCommitStatsProperties
        Helper method for log. Caclulates statistics for each change/commit and
        returns them as a comma seperated string. Log will add these to the commit object
        properties

        @param stats            These are the stats given by --numstat as an array
        @param commitFiles      These are all tracked commit files
        @param devExperience    These are all tracked developer experiences
        @param author           The author of the commit
        @param unixTimeStamp    Time of the commit
        """

        stat_properties = dict()

        # Data structures to keep track of info needed for stats
        subsystemsSeen = []                         # List of system names seen
        directoriesSeen = []                        # List of directory names seen
        locModifiedPerFile = []                     # List of modified loc in each file seen
        authors = []                                # List of all unique authors seen for each file
        fileAges = []                               # List of the ages for each file in a commit

        # Stats variables
        la = 0                                      # lines added
        ld = 0                                      # lines deleted
        nf = 0                                      # Number of modified files
        ns = 0                                      # Number of modified subsystems
        nd = 0                                      # number of modified directories
        entrophy = 0                                # entrophy: distriubtion of modified code across each file
        lt = 0                                      # lines of code in each file (sum) before the commit
        ndev = 0                                    # the number of developers that modifed the files in a commit
        age = 0                                     # the average time interval between the last and current change
        exp = 0                                     # number of changes made by author previously
        rexp = 0                                    # experience weighted by age of files ( 1 / (n + 1))
        sexp = 0                                    # changes made previous by author in same subsystem
        totalLOCModified = 0                        # Total modified LOC across all files
        nuc = 0                                     # number of unique changes to the files
        files_seen = []                             # files seen in change/commit

        for stat in stats:

            if( stat == ' ' or stat == '' ):
                continue

            fileStat = stat.split("\\t")

             # Check that we are only looking at file stat (i.e., remove extra newlines)
            if( len(fileStat) < 2):
                continue

            # catch the git "-" line changes
            try:
                fileLa = int(fileStat[0])
                fileLd = int(fileStat[1])
            except:
                fileLa = 0
                fileLd = 0

            # Remove oddities in filename so we can process it
            fileName = (fileStat[2].replace("'",'').replace('"','').replace("\\",""))

            totalModified = fileLa + fileLd

            # have we seen this file already?
            if(fileName in commitFiles):
                prevFileChanged = commitFiles[fileName]
                prevLOC = getattr(prevFileChanged, 'loc')
                prevAuthors = getattr(prevFileChanged, 'authors')
                prevChanged = getattr(prevFileChanged, 'lastchanged')
                file_nuc = getattr(prevFileChanged, 'nuc')
                nuc += file_nuc
                lt += prevLOC

                for prevAuthor in prevAuthors:
                    if prevAuthor not in authors:
                        authors.append(prevAuthor)

                # Convert age to days instead of seconds
                age += ( (int(unixTimeStamp) - int(prevChanged)) / 86400 )
                fileAges.append(prevChanged)

                # Update the file info

                file_nuc += 1 # file was modified in this commit
                setattr(prevFileChanged, 'loc', prevLOC + fileLa - fileLd)
                setattr(prevFileChanged, 'authors', authors)
                setattr(prevFileChanged, 'lastchanged', unixTimeStamp)
                setattr(prevFileChanged, 'nuc', file_nuc)

            else:

                # new file we haven't seen b4, add it to file commit files dict
                if(author not in authors):
                    authors.append(author)

                if(unixTimeStamp not in fileAges):
                    fileAges.append(unixTimeStamp)

                fileObject = CommitFile(fileName, fileLa - fileLd, authors, unixTimeStamp)
                commitFiles[fileName] = fileObject

            # end of stats loop

            locModifiedPerFile.append(totalModified) # Required for entrophy
            totalLOCModified += totalModified
            fileDirs = fileName.split("/")

            if( len(fileDirs) == 1 ):
                subsystem = "root"
                directory = "root"
            else:
                subsystem = fileDirs[0]
                directory = "/".join(fileDirs[0:-1])

            if( subsystem not in subsystemsSeen ):
                subsystemsSeen.append( subsystem )

            if( author in devExperience ):
                experiences = devExperience[author]
                exp += sum(experiences.values())

                if( subsystem in experiences ):
                    sexp = experiences[subsystem]
                    experiences[subsystem] += 1
                else:
                    experiences[subsystem] = 1

                try:
                    rexp += (1 / (age) + 1)
                except:
                    rexp += 0

            else:
                devExperience[author] = {subsystem: 1}

            if( directory not in directoriesSeen ):
                directoriesSeen.append( directory )

            # Update file-level metrics
            la += fileLa
            ld += fileLd
            nf += 1
            files_seen.append(fileName)

        # End stats loop

        if( nf < 1):
            return ""

        # Update commit-level metrics
        ns = len(subsystemsSeen)
        nd = len(directoriesSeen)
        ndev = len(authors)
        lt = lt / nf
        age = age / nf
        exp = exp / nf
        rexp = rexp / nf

        # Update entrophy
        for fileLocMod in locModifiedPerFile:
            if (fileLocMod != 0 ):
                avg = fileLocMod/totalLOCModified
                entrophy -= ( avg * math.log( avg,2 ) )

        # Add stat properties to the commit object
        stat_properties['la'] = str(la)
        stat_properties['ld'] = str(ld)
        stat_properties['fileschanged'] = json.dumps(files_seen)
        stat_properties['nf'] = str(nf)
        stat_properties['ns'] = str(ns)
        stat_properties['nd'] = str(nd)
        stat_properties['entrophy'] = str(entrophy)
        stat_properties['ndev'] = str(ndev)
        stat_properties['lt'] = str(lt)
        stat_properties['nuc'] = str(nuc)
        stat_properties['age'] = str(age)
        stat_properties['exp'] = str(exp)
        stat_properties['rexp'] = str(rexp)
        stat_properties['sexp'] = str(sexp)

        return stat_properties
    # End stats

    def repository_head_commit(self, repository):
        """
        Returns the hash of the head commit of a specified repository
        :param repository:
        :return:
        """
        repository_path = self.__repository_directory_path__(repository)
        raw_head_hash = str(subprocess.check_output(self.HEAD_COMMIT_HASH_CMD, shell=True, cwd=repository_path))

        if len(raw_head_hash) > 40:
            return raw_head_hash.replace("b'", "")[:40]
        else:
            logging.error("Head commit cannot be extracted from : %s" % repository.name)
            return None

    def log(self, repo):
        """
        log(): Repository, Boolean -> Dictionary
        arguments: repo Repository: the repository to clone
        description: a very basic abstraction for using git in python.
        """
        repo_dir = self.__repository_directory_path__(repo)
        logging.info('Getting/parsing git commits: '+ str(repo) )

        # Spawn a git process and convert the output to a string
        if repo.last_ingested_commit:
            cmd = 'git log %s..HEAD ' % repo.last_ingested_commit
        else:
            cmd = 'git log '

        log = str( subprocess.check_output(cmd + self.LOG_FORMAT, shell=True, cwd = repo_dir ) )
        log = log[2:-1]   # Remove head/end clutter

        # List of json objects
        json_list = []

        # Make sure there are commits to parse
        if len(log) == 0:
            return []

        commitFiles = {}            # keep track of ALL file changes
        devExperience = {}          # Keep track of ALL developer experience
        classifier = Classifier()   # classifier for classifying commits (i.e., corrective, feature addition, etc)

        commitList = log.split("CAS_READER_STARTPRETTY")

        for commit in commitList:
            author = ""                                 # author of commit
            unixTimeStamp = 0                           # timestamp of commit
            fix = False                                 # whether or not the change is a defect fix
            classification = None                       # classification of the commit (i.e., corrective, feature addition, etc)
            isMerge = False                             # whether or not the change is a merge

            commit = commit.replace('\\x', '\\u00')   # Remove invalid json escape characters
            splitCommitStat = commit.split("CAS_READER_STOPPRETTY")  # split the commit info and its stats

            # The first split will contain an empty list
            if(len(splitCommitStat) < 2):
                continue

            prettyCommit = splitCommitStat[0]
            statCommit = splitCommitStat[1]
            commit_object = {}

            # Start with the commit info (i.e., commit hash, author, date, subject, etc)
            prettyInfo = prettyCommit.split(',CAS_READER_PROP_DELIMITER2    "')
            for propValue in prettyInfo:
                props = propValue.split('"CAS_READER_PROP_DELIMITER: "')

                # avoid escapes & newlines for JSON formatting
                key = props[0].replace('\\', '').replace("\\n", '').replace('"', '').strip(' ')
                value = props[1].replace('\\', '').replace("\\n", '').replace('"', '').strip(' ')

                if key == 'parent_hashes':
                    # Check to see if this is a merge change. Fix for Issue #26. 
                    # Detects merges by counting the # of parent commits

                    parents = value.split(' ')
                    if len(parents) == 2:
                        isMerge = True

                if key == 'author_name':
                    author = value.replace('"', '')

                if key == 'author_date_unix_timestamp':
                    unixTimeStamp = value.replace('"', '')

                # Classify the commit
                if key == 'commit_message':

                    if isMerge:
                        classification = "Merge"
                    else:
                        classification = classifier.categorize(value.lower())

                    # If it is a corrective commit, we induce it fixes a bug somewhere in the system
                    if classification == "Corrective":
                        fix = True

                commit_object[key] = value
                # End property loop
            # End pretty info loop

            # Get the stat properties
            stats = statCommit.split("\\n")
            commit_object.update(self.getCommitStatsProperties(stats, commitFiles, devExperience, author, unixTimeStamp))

            # Update the classification of the commit
            commit_object['classification'] = str(classification)

            # Update whether commit was a fix or not
            commit_object['fix'] = str(fix)

            # Assign the commit to it's repository
            commit_object['repository_id'] = repo.id

            # Add commit object to json_list
            json_list.append(commit_object)
        # End commit loop

        logging.info('Done getting/parsing git commits.')
        return json_list

    def clone(self, repo):
        """
        clone(repo): Repository -> String
        description:Takes the current repo and clones it into the
            `clone_directory/the_repo_id`
        arguments: repo Repository: the repository to clone
        pre-conditions: The repo has not been already created
        """
        repo_dir = REPO_DIRECTORY

        # Run the clone command and return the results

        logging.info('Git cloning repo: '+ str(repo) )
        cloneResult = str(subprocess.check_output(
                  self.CLONE_CMD.format(repo.url, './' + repo.id),
                  shell= True,
                  cwd = repo_dir ) )
        logging.info('Done cloning.')
        #logging.debug("Git clone result:\n" + cloneResult)

        # Reset path for next repo

        # TODO: only return true on success, else return false
        return True

    def pull(self, repo):
        """
        fetch(repo): Repository -> String
        description:Takes the current repo and pulls the latest changes.
        arguments: repo Repository: the repository to pull
        pre-conditions: The repo has already been created
        """

        repo_dir = self.__repository_directory_path__(repo)

        # Weird sceneario where something in repo gets modified - reset all changes before pulling
        subprocess.call(self.RESET_CMD, shell=True, cwd= repo_dir)
        subprocess.call(self.CLEAN_CMD, shell=True, cwd= repo_dir)

        # Run the pull command and return the results
        logging.info('Pulling latest changes from repo: '+ str(repo) )
        fetchResult = str(subprocess.check_output(
                  self.RESET_CMD + "\n" + self.PULL_CMD ,
                  shell=True,
                  cwd=  repo_dir  ) )
        logging.info('Done fetching.')
        #logging.debug("Git pull result:\n" + cloneResult)

        # TODO: only return true on success, else return false
        return True

    def __repository_directory_path__(self, repository):
        """
        Return the full path to the directory that contains the git repository
        :param repository:
        :return: repository path
        """
        return os.path.join(REPO_DIRECTORY, repository.id)
