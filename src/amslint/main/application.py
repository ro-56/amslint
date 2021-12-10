"""Module containing the application logic"""
import logging
import time
from typing import Optional
from typing import Type

import amslint
from amslint import exceptions
from amslint import style_guide


LOG = logging.getLogger(__name__)


class Application:
    """Abstract the application into a class."""

    start_time: float
    end_time: Optional[float]
    guide: Optional[style_guide.StyleGuideManager]
    # file_checker_manager
    # guide_plugins:
    # report_formatting_plugins: 
    catastrophic_failure: bool


    def __init__(self):
        """Initialize the application.
        """
        #: The timestamp when the Application instance was instantiated.
        self.start_time = time.time()
        #: The timestamp when the Application finished reported errors.
        self.end_time: Optional[float] = None

        # #: The instance of :class:`flake8.plugins.manager.Checkers`
        # self.check_plugins: Optional[plugin_manager.Checkers] = None
        
        # #: The instance of :class:`flake8.plugins.manager.ReportFormatters`
        # self.report_formatting_plugins: Optional[
        #     plugin_manager.ReportFormatters
        # ] = None
        
        #: The :class:`flake8.style_guide.StyleGuideManager` built from the
        #: user's options
        self.guide: Optional[style_guide.StyleGuideManager] = None
        
        # #: The :class:`flake8.checker.Manager` that will handle running all of
        # #: the checks selected by the user.
        # self.file_checker_manager: Optional[checker.Manager] = None

        #: Whether or not something catastrophic happened and we should exit
        #: with a non-zero status code
        self.catastrophic_failure = False

        self.message_manager = None

    def make_guide(self) -> None:
        """Initialize our StyleGuide."""
        # self.guide = style_guide.StyleGuideManager(
        #     self.options, self.formatter
        # )

    def make_file_checker_manager(self) -> None:
        """Initialize our FileChecker Manager."""
        # self.file_checker_manager = checker.Manager(
        #     style_guide=self.guide
        # )

    def initialize(self) -> None:
        """Initialize the application to be run."""
        self.make_guide()
        self.make_file_checker_manager()

    def run_checks(self) -> None:
        pass
        # """Run the actual checks with the FileChecker Manager.
        # This method encapsulates the logic to make a
        # :class:`~flake8.checker.Manger` instance run the checks it is
        # managing.
        # """
        # assert self.options is not None
        # assert self.file_checker_manager is not None
        # if self.options.diff:
        #     files: Optional[list[str]] = sorted(self.parsed_diff)
        #     if not files:
        #         return
        # else:
        #     files = None

        # self.file_checker_manager.start(files)
        # try:
        #     self.file_checker_manager.run()
        # except exceptions.PluginExecutionFailed as plugin_failed:
        #     print(str(plugin_failed))
        #     print("Run flake8 with greater verbosity to see more details")
        #     self.catastrophic_failure = True
        # LOG.info("Finished running")
        # self.file_checker_manager.stop()
        # self.end_time = time.time()

    def report(self) -> None:
        pass

    def _run(self) -> None:
        self.initialize()
        self.run_checks()
        self.report()

    def run(self) -> None:
        """Run our application.
        This method will also handle KeyboardInterrupt exceptions for the
        entirety of the flake8 application. If it sees a KeyboardInterrupt it
        will forcibly clean up the :class:`~flake8.checker.Manager`.
        """
        try:
            self._run()
        except KeyboardInterrupt as exc:
            print("... stopped")
            LOG.critical("Caught keyboard interrupt from user")
            LOG.exception(exc)
            self.catastrophic_failure = True
        except exceptions.ExecutionError as exc:
            print("There was a critical error during execution of Flake8:")
            print(exc)
            LOG.exception(exc)
            self.catastrophic_failure = True