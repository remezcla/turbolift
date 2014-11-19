# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================

from cloudlib import logger

from turbolift import utils
from turbolift import methods

LOG = logger.getLogger('turbolift')


class DeleteRunMethod(methods.BaseMethod):
    """Setup and run the list Method."""

    def __init__(self, job_args):
        super(DeleteRunMethod, self).__init__(job_args)

    def start(self):
        indicator_options = {
            'debug': self.debug,
            'quiet': self.quiet,
            'msg': ' Deleting... '
        }
        with utils.IndicatorThread(**indicator_options):
            # Perform the delete twice
            user_defined, _objects = self._return_container_objects()
            while _objects:
                self._multi_processor(
                    self._delete,
                    items=_objects
                )
                if not user_defined:
                    user_defined, _objects = self._return_container_objects()

            # Delete the container unless instructed to save it
            if not self.job_args.get('save_container') or not user_defined:
                self._delete()
