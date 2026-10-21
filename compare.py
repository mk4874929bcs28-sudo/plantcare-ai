import glob
import numpy as np
from PIL import Image
import tensorflow as tf

KERAS_FILE = "plant_disease_model.keras"
TFLITE_FILE = "plant_disease_model.tflite"

# Vera vera plant / disease images (file name la irukkura code)
PATTERNS = ["HLB", "C.Rust", "Bact.S", "SpM", "RS_Rust"]

images = []
for p in PATTERNS:
    found = glob.glob(f"static/uploads/*{p}*.JPG")
    if found:
        images.append(found[0])

keras_model = tf.keras.models.load_model(KERAS_FILE)

interp = tf.lite.Interpreter(model_path=TFLITE_FILE)
interp.allocate_tensors()
inp = interp.get_input_details()[0]
out = interp.get_output_details()[0]
print("TFLITE input :", inp["shape"], inp["dtype"])
print("TFLITE output:", out["shape"], out["dtype"])
print("-" * 50)

for path in images:
    img = Image.open(path).convert("RGB").resize((224, 224))
    x = np.expand_dims(np.array(img, dtype=np.float32), axis=0)

    k = keras_model.predict(x, verbose=0)[0]

    interp.set_tensor(inp["index"], x)
    interp.invoke()
    t = interp.get_tensor(out["index"])[0]

    print("IMAGE :", path.split("___")[-1])
    print("  KERAS :", int(np.argmax(k)), round(float(np.max(k)) * 100, 2))
    print("  TFLITE:", int(np.argmax(t)), round(float(np.max(t)) * 100, 2))