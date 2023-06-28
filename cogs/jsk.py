from disnake.ext import commands
import jishaku
from jishaku.features.python import PythonFeature
from jishaku.features.root_command import RootCommand
from jishaku.features.shell import ShellFeature
from jishaku.features.management import ManagementFeature
from jishaku.features.invocation import InvocationFeature

class CustomDebugCog(PythonFeature, ShellFeature, 
                     ManagementFeature, InvocationFeature,
                     RootCommand):
    pass

def setup(bot: commands.Bot):
    jishaku.Flags.NO_UNDERSCORE = True
    jishaku.Flags.NO_DM_TRACEBACK = True
    jishaku.Flags.FORCE_PAGINATOR = True
    bot.add_cog(CustomDebugCog(bot=bot))