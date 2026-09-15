import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Dataset paths
train_dir = r"C:\PlantCareDataset\dataset\PlantVillage\PlantVillage\train"
val_dir = r"C:\PlantCareDataset\dataset\PlantVillage\PlantVillage\val"

# Image settings
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Load training dataset
train_ds = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True
)

# Load validation dataset
val_ds = tf.keras.utils.image_dataset_from_directory(
    val_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

# Get class names
class_names = train_ds.class_names

print("\nClasses found:")
for i, name in enumerate(class_names):
    print(i, name)

print("\nTotal classes:", len(class_names))

# Improve performance
AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

# Data augmentation
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# Transfer learning model
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

# Freeze pretrained layers
base_model.trainable = False

# Build model
model = models.Sequential([
    data_augmentation,

    layers.Rescaling(1./127.5, offset=-1),

    base_model,

    layers.GlobalAveragePooling2D(),

    layers.Dropout(0.3),

    layers.Dense(len(class_names), activation="softmax")
])

# Compile
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Save best model
checkpoint = ModelCheckpoint(
    "plant_disease_model.keras",
    monitor="val_accuracy",
    save_best_only=True,
    verbose=1
)

# Stop if validation accuracy stops improving
early_stop = EarlyStopping(
    monitor="val_accuracy",
    patience=3,
    restore_best_weights=True
)

# Train
print("\nStarting training...\n")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10,
    callbacks=[checkpoint, early_stop]
)

# Save final model
model.save("plant_disease_model.keras")

# Save class names
with open("class_names.txt", "w") as f:
    for name in class_names:
        f.write(name + "\n")

print("\nTraining completed!")
print("Model saved as: plant_disease_model.keras")
print("Classes saved as: class_names.txt")