from data_loader import get_datasets, get_augmentation_layer
from model import build_model, prepare_for_fine_tuning
from evaluate import plot_history, evaluate_and_report
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
import os

EPOCHS_PHASE1 = 15
EPOCHS_PHASE2 = 25
MODEL_SAVE_PATH = 'waste_classification_model.h5'

def main():
    train_ds, val_ds, class_names = get_datasets()
    num_classes = len(class_names)
    augmentation = get_augmentation_layer()
    model, base_model = build_model(num_classes, augmentation)
    lr_reduction = ReduceLROnPlateau(monitor='val_loss', patience=3, verbose=1, factor=0.5, min_lr=1e-06)
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1)
    
    history_phase1 = model.fit(train_ds, epochs=EPOCHS_PHASE1, validation_data=val_ds, callbacks=[lr_reduction, early_stop])
    
    model = prepare_for_fine_tuning(model, base_model)
    history_phase2 = model.fit(train_ds, epochs=EPOCHS_PHASE1 + EPOCHS_PHASE2, initial_epoch=history_phase1.epoch[-1] + 1, validation_data=val_ds, callbacks=[lr_reduction, early_stop])
    
    model.save(MODEL_SAVE_PATH)
    
    try:
        plot_history(history_phase1, history_phase2, len(history_phase1.epoch))
    except:
        pass
        
    evaluate_and_report(val_ds, class_names)

if __name__ == '__main__':
    main()
