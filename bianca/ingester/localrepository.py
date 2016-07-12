"""
file: localrepository.py
author: Ben Grawi <bjg1568@rit.edu>
date: October 2013
description: Holds the repository abstraction class
"""
from ingester.git import *
from orm.commit import *
from datetime import datetime
import os
import logging


class LocalRepository:
    """
    Repository():
    description: Abstracts the actions done on a repository
    """
    repo = None
    adapter = None
    start_date = None
    head_commit_hash = None

    def __init__(self, repo):
        """
        __init__(path): String -> NoneType
        description: Abstracts the actions done on a repository
        """
        self.repo = repo

        # Temporary until other Repo types are added
        self.adapter = Git()

        self.commits = {}

    def sync(self):
        """
        sync():
        description: Simply wraps the syncing functions together
        """

        # TODO: Error checking.
        self.syncRepoFiles()
        self.syncCommits()

        # Set the date AFTER it has been ingested and synced.
        self.repo.ingestion_date = self.start_date
        self.repo.last_ingested_commit = self.head_commit_hash

    def syncRepoFiles(self):
        """
        syncRepoFiles() -> Boolean
        description: Downloads the current repo locally, and sets the path and
            injestion date accordingly
        returns: Boolean - if this is the first sync
        """
        # Cache the start date to set later
        self.start_date = str(datetime.now().replace(microsecond=0))

        path = os.path.join(REPO_DIRECTORY, self.repo.id)
        # See if repo has already been downloaded, if it is pull, if not clone
        if os.path.isdir(path):
            self.adapter.pull(self.repo)
        else:
            self.adapter.clone(self.repo)

    def syncCommits(self):
        """
        syncCommits():
        description: Makes each commit dictonary into an object and then
            inserts them into the database
        """
        commits = self.adapter.log(self.repo)
        self.head_commit_hash = self.adapter.repository_head_commit(self.repo)

        commitsSession = Session()
        logging.info('Saving commits to the database...')
        for commitDict in commits:

            # We have already ingested the previous commit so we don't want to add it again
            if self.repo.last_ingested_commit:
                pass
            # commitDict['repository_id'] = self.repo.id
            # commitsSession.merge(Commit(commitDict))
            commitsSession.add(Commit(commitDict))
        commitsSession.commit()
        commitsSession.close()
        logging.info('Done saving commits to the database.')
