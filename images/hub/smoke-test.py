# Run by CI inside the built image (not copied into it).
import jupyterhub, kubespawner, jupyterhub_fancy_profiles
from jupyterhub_fancy_profiles import setup_ui
from traitlets.config import Config

c = Config()
setup_ui(c)  # the exact call rp1-core's hub extraConfig makes
assert c.KubeSpawner.additional_profile_form_template_paths, "fancy-profiles templates not registered"

print("jupyterhub", jupyterhub.__version__, "kubespawner", kubespawner.__version__)
