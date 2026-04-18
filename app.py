from flask import Flask, request, jsonify
from emi_calculator import calculate_emi
from database import SessionLocal
from models import Loan
app = Flask(__name__)

@app.route("/")
def home():
    return "EMI Backend Running 🚀"

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json

    principal = data["principal"]
    rate = data["rate"]
    tenure = data["tenure"]

    emi = calculate_emi(principal, rate, tenure)

    # 🔥 SAVE TO DATABASE
    db = SessionLocal()

    new_loan = Loan(
        principal=principal,
        rate=rate,
        tenure=tenure,
        emi=emi
    )

    db.add(new_loan)
    db.commit()
    db.close()

    return jsonify({"emi": emi})



@app.route("/loans", methods=["GET"])
def get_loans():
    db = SessionLocal()

    loans = db.query(Loan).all()

    result = []
    for loan in loans:
        result.append({
            "id": loan.id,
            "principal": loan.principal,
            "rate": loan.rate,
            "tenure": loan.tenure,
            "emi": loan.emi
        })

    db.close()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
