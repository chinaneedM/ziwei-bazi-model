from __future__ import annotations

import unittest

from fortune_training.combined_chart_application.local_app import APP_JS


class CombinedChartFailedRequestResetUiR1Tests(unittest.TestCase):
    def test_failed_request_reset_clears_prior_resolution_identity(self) -> None:
        self.assertIn("function resetRenderedResolution(){", APP_JS)
        self.assertIn("last=null;", APP_JS)
        self.assertIn("$('manifest-hash').textContent='-';", APP_JS)
        self.assertIn("$('manifest-hash').removeAttribute('title');", APP_JS)
        self.assertIn("$('ziwei-status').textContent='-';", APP_JS)
        self.assertIn("$('ziwei-hash').textContent='-';", APP_JS)
        self.assertIn("$('bazi-status').textContent='-';", APP_JS)
        self.assertIn("$('bazi-hash').textContent='-';", APP_JS)

    def test_failed_request_reset_clears_prior_subsystem_presentation(self) -> None:
        self.assertIn("showSubError('ziwei-error',null);", APP_JS)
        self.assertIn("showSubError('bazi-error',null);", APP_JS)
        self.assertIn("zroot.textContent='当前请求未产生紫微结果';", APP_JS)
        self.assertIn("broot.textContent='当前请求未产生八字结果';", APP_JS)

    def test_request_failure_invokes_reset_before_global_error(self) -> None:
        catch_marker = "}catch(error){resetRenderedResolution(); $('combined-status').textContent='失败';"
        self.assertIn(catch_marker, APP_JS)
        self.assertIn("$('global-error').hidden=false;", APP_JS)
        self.assertIn("['download-manifest','download-ziwei','download-bazi'].forEach((id)=>$(id).disabled=true);", APP_JS)


if __name__ == "__main__":
    unittest.main()
