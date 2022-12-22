from multiprocessing.pool import ThreadPool
from pathlib import Path


import os
import shutil
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

class MultithreadedCopier:
    def __init__(self, max_threads):
        self.pool = ThreadPool(max_threads)
        self.progress: Progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            MofNCompleteColumn(),
        )
        self.task = self.progress.add_task(
            "Processing",total=None
        )
        self.progress.update(self.task, advance=0.5)

    def copy(self, source, dest):
       
        self.progress.update(self.task, advance=0.5)
        self.pool.apply_async(shutil.copy2, args=(source, dest))


    def __enter__(self):
        self.progress.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.close()
        self.pool.join()
        self.progress.console.clear_live()
        self.progress.stop()
        (self.progress.remove_task(i.id) for i in self.progress.tasks)
        
        
def main():
    sourceDir = Path("")
    destinationDir = Path("")
    if Path(destinationDir).exists():
        print("Deleting Folder")
        shutil.rmtree(destinationDir, ignore_errors=True)
    with MultithreadedCopier(max_threads=5) as copier:
        try:
            shutil.copytree(sourceDir, destinationDir,copy_function=copier.copy)
        except OSError:
            shutil.copy(sourceDir, destinationDir)


if __name__ == "__main__":
    main()