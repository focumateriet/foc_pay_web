from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from foc_pay_web.payments.api.serializers import PaymentSerializer
from foc_pay_web.payments.models import Payment


class PaymentViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    @action(detail=False)
    def get_paid_focumama_payment(self, request):
        paid_focumama_payment = Payment.paid.filter(machine=Payment.MACHINES.focumama).first()
        if paid_focumama_payment:
            serializer = self.get_serializer(paid_focumama_payment)
            return Response(serializer.data)
        else:
            return Response(None)

    @action(detail=False)
    def get_paid_drickomaten_payment(self, request):
        paid_drickomaten_payment = Payment.paid.filter(machine=Payment.MACHINES.drickomaten).first()
        if paid_drickomaten_payment:
            serializer = self.get_serializer(paid_drickomaten_payment)
            return Response(serializer.data)
        else:
            return Response(None)

    @action(detail=True, methods=["post"])
    def credit_payment(self, request, pk=None):
        payment: Payment = self.get_object()
        payment.status = Payment.STATUS.credited
        payment.save()
        serializer = self.get_serializer(payment)
        return Response(serializer.data)
