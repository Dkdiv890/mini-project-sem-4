from data_loader import get_datasets, get_augmentation_layer
from model import build_model, prepare_for_fine_tuning
from evaluate import plot_history, evaluate_and_report
EPOCHS_PHASE1 = 5
EPOCHS_PHASE2 = 5
MODEL_SAVE_PATH = 'waste_classification_model.h5'

def main():
    print('=' * 55)
    print('  Waste Classification – CNN Fine-Tuning Pipeline')
    print('=' * 55)
    print('\n[Step 1] Loading and preprocessing dataset...')
    train_ds, val_ds, class_names = get_datasets()
    num_classes = len(class_names)
    print('\n[Step 2] Building model...')
    augmentation = get_augmentation_layer()
    model, base_model = build_model(num_classes, augmentation)
    model.summary()
    print(f'\n[Step 3] Phase 1 – Feature Extraction  ({EPOCHS_PHASE1} epochs)')
    print('         Base MobileNetV2 layers are FROZEN.')
    history_phase1 = model.fit(train_ds, epochs=EPOCHS_PHASE1, validation_data=val_ds)
    print(f'\n[Step 4] Phase 2 – Fine-Tuning  ({EPOCHS_PHASE2} more epochs)')
    print('         Top layers of MobileNetV2 are UNFROZEN with very low LR.')
    model = prepare_for_fine_tuning(model, base_model)
    model.summary()
    history_phase2 = model.fit(train_ds, epochs=EPOCHS_PHASE1 + EPOCHS_PHASE2, initial_epoch=history_phase1.epoch[-1] + 1, validation_data=val_ds)
    print(f"\n[Step 5] Saving model → '{MODEL_SAVE_PATH}'")
    model.save(MODEL_SAVE_PATH)
    print(f'         Model saved successfully.')
    print('\n[Step 6] Generating performance plots...')
    plot_history(history_phase1, history_phase2, EPOCHS_PHASE1)
    print('\n[Step 7] Evaluating model on validation set...')
    evaluate_and_report(val_ds, class_names)
    print('\n' + '=' * 55)
    print('  Training complete!')
    print(f'  ✔ Model   → {MODEL_SAVE_PATH}')
    print('  ✔ Plot    → performance_evaluation.png')
    print('  ✔ Report  → classification_report.txt')
    print('=' * 55)
if __name__ == '__main__':
    main()