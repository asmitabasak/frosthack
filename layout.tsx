import { Slot } from 'expo-router';
import { useEffect } from 'react';
import { useFonts } from 'expo-font';
import { View, Text, SafeAreaView } from 'react-native';

export default function Layout() {
    return (
        <SafeAreaView style={{ flex: 1 }}>
            <Slot />
        </SafeAreaView>
    );
}