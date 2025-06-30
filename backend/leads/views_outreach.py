from rest_framework.response import Response
from rest_framework.views import APIView

from .services.outreach import run_outreach


class StartOutreachView(APIView):
    """
    Trigger the outreach loop manually.
    """

    def post(self, request):
        processed_ids = run_outreach()
        return Response(
            {
                "processed": processed_ids,
                "message": f"Outreach completed for {len(processed_ids)} lead(s).",
            }
        )
