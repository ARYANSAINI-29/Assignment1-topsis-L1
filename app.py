from flask import Flask, request, render_template, send_file
import pandas as pd
import io
import sys
import os

# Ensure the current directory is in sys.path to resolve imports
sys.path.append(os.getcwd())

from topsis_aryan.run_topsis import calculate_topsis

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
            
        weights_input = request.form['weights']
        impacts_input = request.form['impacts']
        # Email is collected but not actively used in this demo version
        # email = request.form['email'] 
        
        try:
            # Parse inputs
            weights = [float(w.strip()) for w in weights_input.split(',')]
            impacts = [i.strip() for i in impacts_input.split(',')]
            
            # Read CSV
            df = pd.read_csv(file)
            
            # Run TOPSIS
            result = calculate_topsis(df, weights, impacts)
            
            # Prepare output
            output = io.BytesIO()
            result.to_csv(output, index=False)
            output.seek(0)
            
            return send_file(
                output, 
                mimetype="text/csv", 
                as_attachment=True, 
                download_name="result.csv"
            )
            
        except Exception as e:
            return f"Error encountered: {str(e)}"
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
